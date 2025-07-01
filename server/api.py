from fastapi import FastAPI, HTTPException
from sse_starlette.sse import EventSourceResponse
import json
import asyncio
import uuid
from datetime import datetime
from contextlib import asynccontextmanager

from .models import (
    Config, ProcessResponse, ClientConnectResponse, ClientTaskResponse, 
    ProjectSetupRequest, ProjectSetupResponse, ProjectWorkflowGenerationRequest, ProjectWorkflowGenerationResponse,
    ProjectWorkflowExecutionRequest, ProjectWorkflowExecutionResponse
)
from .service import (
    handle_process_request, start_streaming_task, setup_project, get_project, list_projects, 
    generate_workflow_for_project, execute_workflow_for_project
)
from .db import initialize_database, close_database, seed_database
from .task_manager import (
    get_stream_task, get_stream_task_updates, is_stream_task_completed,
    create_client_session, get_client_session, get_client_updates, 
    is_client_session_active, add_task_to_client, send_to_client
)

app = FastAPI(title="Processing Server")

@app.post("/process", response_model=ProcessResponse)
async def process_request(config: Config) -> ProcessResponse:
    """
    Process the incoming request with the given configuration.
    Returns a task ID that can be used to retrieve results.
    """
    try:
        return await handle_process_request(config.parameters)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Updated workflow-based endpoints (using original project endpoints)
@app.post("/project/setup", response_model=ProjectSetupResponse)
async def setup_new_project(request: ProjectSetupRequest) -> ProjectSetupResponse:
    """
    Phase 1: Setup workflow and generate task_info.
    This is the first phase of the workflow process.
    """
    try:
        result = await setup_project(request.workflow_id, request.requirement_id, request.user_id)
        return ProjectSetupResponse(task_info=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error setting up workflow: {str(e)}")

@app.post("/workflow/generate", response_model=ProjectWorkflowGenerationResponse)
async def generate_workflow_for_project_api(request: ProjectWorkflowGenerationRequest) -> ProjectWorkflowGenerationResponse:
    """
    Phase 2: Generate workflow graph based on task_info.
    This is the second phase of the workflow process.
    """
    try:
        result = await generate_workflow_for_project(request.workflow_id)
        return ProjectWorkflowGenerationResponse(
            workflow_graph=result["workflow_graph"],
            status=result["status"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating workflow: {str(e)}")

@app.post("/workflow/execute", response_model=ProjectWorkflowExecutionResponse)
async def execute_workflow_for_project_api(request: ProjectWorkflowExecutionRequest) -> ProjectWorkflowExecutionResponse:
    """
    Phase 3: Execute workflow with provided inputs.
    This is the third phase of the workflow process.
    """
    try:
        result = await execute_workflow_for_project(request.workflow_id, request.inputs)
        return ProjectWorkflowExecutionResponse(execution_result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing workflow: {str(e)}")

# Workflow management endpoints
@app.get("/workflow/{workflow_id}/status")
async def get_workflow_status(workflow_id: str):
    """
    Get the current status and details of a workflow.
    Shows which phase the workflow is in and all stored data.
    """
    try:
        workflow = await get_project(workflow_id)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        return {
            "workflow_id": workflow_id,
            "status": workflow.get("status", "unknown"),
            "user_id": workflow.get("user_id"),
            "requirement_id": workflow.get("requirement_id"),
            "created_at": workflow.get("created_at"),
            "updated_at": workflow.get("updated_at"),
            "phases": {
                "setup_complete": workflow.get("task_info") is not None,
                "generation_complete": workflow.get("workflow_graph") is not None,
                "execution_complete": workflow.get("execution_result") is not None
            },
            "task_info": workflow.get("task_info"),
            "workflow_graph": workflow.get("workflow_graph"),
            "execution_result": workflow.get("execution_result")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting workflow status: {str(e)}")

@app.get("/workflows")
async def get_all_workflows():
    """
    List all workflows in the system with their current status.
    """
    try:
        workflows_info = await list_projects()
        
        # Get detailed info for each workflow
        detailed_workflows = []
        for workflow_id in workflows_info["projects"]:
            workflow = await get_project(workflow_id)
            if workflow:
                detailed_workflows.append({
                    "workflow_id": workflow_id,
                    "status": workflow.get("status", "unknown"),
                    "user_id": workflow.get("user_id"),
                    "requirement_id": workflow.get("requirement_id"),
                    "created_at": workflow.get("created_at"),
                    "updated_at": workflow.get("updated_at"),
                    "phases_complete": {
                        "setup": workflow.get("task_info") is not None,
                        "generation": workflow.get("workflow_graph") is not None,
                        "execution": workflow.get("execution_result") is not None
                    }
                })
        
        return {
            "workflows": detailed_workflows,
            "total_count": workflows_info["total_count"],
            "active_workflows": workflows_info["active_projects"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing workflows: {str(e)}")

@app.post("/stream/process")
async def start_stream_process(config: Config):
    """
    Start a streaming process and return a task ID.
    """
    return await start_streaming_task(config.dict())

# New client-session endpoints
@app.post("/connect", response_model=ClientConnectResponse)
async def connect_client() -> ClientConnectResponse:
    """
    Create a new client session and return client ID with stream URL.
    """
    client_id = str(uuid.uuid4())
    create_client_session(client_id)
    
    return ClientConnectResponse(
        client_id=client_id,
        stream_url=f"/stream/client/{client_id}"
    )

@app.get("/stream/client/{client_id}")
async def stream_client_updates(client_id: str):
    """
    Persistent SSE stream for a client session.
    """
    if not get_client_session(client_id):
        raise HTTPException(status_code=404, detail="Client session not found")
        
    return EventSourceResponse(
        client_event_generator(client_id, timeout=3600)  # 1 hour timeout
    )

@app.delete("/client/{client_id}")
async def disconnect_client(client_id: str):
    """
    Disconnect a client session.
    """
    if not get_client_session(client_id):
        raise HTTPException(status_code=404, detail="Client session not found")
    
    from .task_manager import close_client_session
    close_client_session(client_id)
    
    return {"status": "disconnected", "client_id": client_id}

async def event_generator(task_id: str, timeout: int = 30):
    """Generate SSE events for a given task"""
    start_time = datetime.now()
    last_index = 0
    
    while True:
        # Check timeout
        if (datetime.now() - start_time).seconds > timeout:
            yield {
                "event": "error",
                "data": json.dumps({"error": "Stream timeout"})
            }
            break
            
        # Check if task exists
        if not get_stream_task(task_id):
            yield {
                "event": "error",
                "data": json.dumps({"error": "Task not found"})
            }
            break
            
        # Get new updates
        updates = get_stream_task_updates(task_id, last_index)
        for update in updates:
            yield {
                "event": "update" if not is_stream_task_completed(task_id) else "complete",
                "data": json.dumps(update)
            }
            last_index += 1
            
        # If task is completed, end stream
        if is_stream_task_completed(task_id):
            break
            
        # Wait before checking for new updates
        await asyncio.sleep(0.5)

async def client_event_generator(client_id: str, timeout: int = 3600):
    """Generate SSE events for a client session"""
    start_time = datetime.now()
    last_index = 0
    
    while True:
        # Check if client session is still active
        if not is_client_session_active(client_id):
            yield {
                "event": "session_closed",
                "data": json.dumps({"message": "Client session closed"})
            }
            break
            
        # Check timeout
        if (datetime.now() - start_time).seconds > timeout:
            yield {
                "event": "session_timeout",
                "data": json.dumps({"message": "Session timed out"})
            }
            break
        
        # Get new updates for this client
        updates = get_client_updates(client_id, last_index)
        for update in updates:
            event_type = update.get("event_type", "update")
            yield {
                "event": event_type,
                "data": json.dumps(update)
            }
            last_index += 1
        
        # Wait before checking for new updates
        await asyncio.sleep(0.5)

@app.get("/stream/{task_id}")
async def stream_results(task_id: str):
    """
    Stream results for a given task ID using Server-Sent Events.
    """
    if not get_stream_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
        
    task_config = get_stream_task(task_id)["config"]
    return EventSourceResponse(
        event_generator(task_id, timeout=task_config["timeout"])
    )

@app.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {"status": "healthy"}

@app.get("/debug/database")
async def debug_database():
    """Debug endpoint to view database contents"""
    from .db import database
    
    if not database:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    try:
        result = {
            "users": await database.find_many("users", limit=50),
            "requirements": await database.find_many("requirements", limit=50), 
            "workflows": await database.find_many("workflows", limit=50),
            "workflow_templates": await database.find_many("workflow_templates", limit=50)
        }
        
        # Add counts
        result["counts"] = {
            "users": await database.count("users"),
            "requirements": await database.count("requirements"),
            "workflows": await database.count("workflows"), 
            "workflow_templates": await database.count("workflow_templates")
        }
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading database: {str(e)}")

@app.get("/clients")
async def list_clients():
    """List all active client sessions (for debugging)"""
    from .task_manager import client_sessions
    active_clients = []
    
    for client_id, session in client_sessions.items():
        if session["is_active"]:
            active_clients.append({
                "client_id": client_id,
                "created_at": session["created_at"].isoformat(),
                "last_activity": session["last_activity"].isoformat(),
                "active_tasks": session["active_tasks"]
            })
    
    return {"active_clients": active_clients, "total": len(active_clients)} 

@app.get("/project/{project_id}/status")
async def get_project_status(project_id: str):
    """
    Get the current status and information for a specific project.
    """
    project = await get_project(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "project_id": project_id,
        "status": project.get("status", "unknown"),
        "goal": project.get("goal", ""),
        "created_at": project.get("created_at", ""),
        "workflow_generated": project.get("workflow_generated", False),
        "workflow_executed": project.get("workflow_executed", False),
        "public_url": project.get("public_url", "Not available"),
        "last_updated": project.get("last_updated", project.get("created_at", ""))
    }

@app.get("/projects")
async def get_all_projects():
    """
    List all projects in the system.
    """
    return await list_projects() 