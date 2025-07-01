import aiohttp
import asyncio
import json
import requests
import os
from dotenv import load_dotenv
import uuid

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# =============================================================================
# WORKFLOW-BASED TESTS - GAOKAO SCORE ESTIMATION (THREE-PHASE STRUCTURE)
# =============================================================================

"""
Complete Gaokao Score Estimation Workflow Test Example (Updated Structure):

=== THREE-PHASE WORKFLOW PROCESS ===

1. PHASE 1 - SETUP INPUT:
{
  "workflow_id": "gaokao-estimation-001",
  "requirement_id": "req-gaokao-2024",
  "user_id": "test-user-123"
}

2. PHASE 2 - GENERATION INPUT:
{
  "workflow_id": "gaokao-estimation-001"
}

3. PHASE 3 - EXECUTION INPUT (WITH INPUTS):
{
  "workflow_id": "gaokao-estimation-001", 
  "inputs": {
    "goal": "Math: 80, English: 120, Physics: 120"
  }
}

=== EXPECTED OUTPUTS ===

1. PROJECT SETUP OUTPUT:
{
  "project_id": "proj_abc123def456",
  "public_url": "https://example.ngrok.io",
  "task_info": "Add ALEX ..."
}

2. WORKFLOW GENERATION OUTPUT:
{
  "success": true,
  "project_id": "proj_abc123def456",
  "workflow_graph": {
    "nodes": [...4 workflow nodes...],
    "edges": [...workflow connections...],
    "goal": "Create a stock price and trend analysis workflow...",
    "description": "Generated workflow for stock analysis"
  }
}

3. WORKFLOW EXECUTION OUTPUT:
{
  "success": true,
  "project_id": "proj_abc123def456",
  "execution_result": {
    "status": "completed",
    "message": "# Comprehensive Report: AAPL Stock Performance Analysis\n\n### 1. Current Price Metrics\n- **Stock Symbol**: AAPL\n- **Latest Stock Price**: $175.30\n- **Market Capitalization**: $2.8 Trillion\n- **Volume Traded**: 95 Million Shares\n\n### 2. Historical Price Data (Last 5 Years)\n- **Average Price**: $150.45\n- **Peak Price**: $182.50 (November 2021)\n- **Low Price**: $84.80 (March 2020)\n- **Volatility**: Notable fluctuations during earnings releases...\n\n### 3. Key Performance Metrics\n- **1-Year Change**: +15%\n- **5-Year Change**: +20%\n- **Dividend Yield**: 0.55%\n\n### 4. Technical Indicators\n- **50-day Moving Average**: $170.00\n- **200-day Moving Average**: $160.00\n- **RSI**: 65 (nearing overbought)\n- **MACD**: Positive divergence\n\n### 5. Recommendations\n- Strong buy recommendation based on solid fundamentals\n- Consider adding positions on market dips\n- Monitor economic indicators for potential impacts\n\n### Conclusion\nAPPL presents a compelling investment opportunity with consistent performance, positive market sentiment, and sound fundamentals.",
    "workflow_received": true,
    "llm_config_received": true,
    "mcp_config_received": false
  },
  "message": "Workflow executed successfully for project",
  "timestamp": "2024-06-18T11:25:02.789000"
}
"""

def test_health_check():
    """Test basic health check endpoint"""
    print("\n=== Testing Health Check ===")
    
    response = requests.get('http://localhost:8001/health')
    assert response.status_code == 200
    
    data = response.json()
    print("✅ Health check passed:", data)
    return data

def test_project_setup():
    """
    Test project setup for Gaokao score estimation website workflow
    Updated to use new workflow structure with workflow_id
    
    Curl command:
    ```bash
    curl -X POST http://localhost:8001/project/setup \
      -H "Content-Type: application/json" \
      -d '{
        "workflow_id": "gaokao-estimation-001",
        "requirement_id": "req-gaokao-2024",
        "user_id": "test-user-123"
      }'
    ```
    """
    print("\n=== Testing Project Setup - Gaokao Score Estimation (Updated Structure) ===")
    
    # Generate unique workflow ID
    workflow_id = f"gaokao-estimation-{str(uuid.uuid4())[:8]}"
    
    project_request = {
        "workflow_id": workflow_id,
        "requirement_id": "req-gaokao-2024",
        "user_id": "test-user-123"
    }
    
    print(f"🚀 Setting up Gaokao score estimation workflow...")
    print(f"   Workflow ID: {workflow_id}")
    print(f"   Requirement ID: {project_request['requirement_id']}")
    print(f"   User ID: {project_request['user_id']}")
    
    response = requests.post('http://localhost:8001/project/setup', json=project_request)
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"✅ Workflow setup completed successfully!")
        print(f"📋 Task info generated with {len(result.get('task_info', {}))} fields")
        
        # Return both for compatibility
        return {
            "workflow_id": workflow_id,
            "project_id": workflow_id,  # For backward compatibility
            "task_info": result.get('task_info')
        }
    else:
        print(f"❌ Workflow setup failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def test_project_status(project_id):
    """Test retrieving workflow status using workflow_id"""
    print(f"\n=== Testing Workflow Status for {project_id} ===")
    
    # Use workflow status endpoint
    response = requests.get(f'http://localhost:8001/workflow/{project_id}/status')
    
    if response.status_code == 200:
        status = response.json()
        
        print(f"✅ Workflow status retrieved:")
        print(f"   Status: {status.get('status', 'unknown')}")
        phases = status.get('phases', {})
        print(f"   Setup Complete: {phases.get('setup_complete', False)}")
        print(f"   Generation Complete: {phases.get('generation_complete', False)}")
        print(f"   Execution Complete: {phases.get('execution_complete', False)}")
        
        return status
    else:
        print(f"❌ Failed to get workflow status: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def test_project_workflow_generation(project_id):
    """
    Test workflow generation for Gaokao score estimation project
    Updated to use workflow_id
    
    Curl command:
    ```bash
    curl -X POST http://localhost:8001/workflow/generate \
      -H "Content-Type: application/json" \
      -d '{
        "workflow_id": "gaokao-estimation-001"
      }'
    ```
    """
    print(f"\n=== Testing Gaokao Score Estimation Workflow Generation for {project_id} ===")
    
    generation_request = {
        "workflow_id": project_id,  # Using workflow_id for server
    }
    
    print(f"🚀 Generating Gaokao score estimation workflow...")
    print(f"   Using workflow_id: {project_id}")
    print(f"   Getting goal and specifications from task_info")
    
    response = requests.post('http://localhost:8001/workflow/generate', json=generation_request)
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"✅ Workflow generated successfully!")
        print(f"   Status: {result.get('status', 'unknown')}")
        print(f"   Workflow graph available: {result.get('workflow_graph') is not None}")
        
        return result
    else:
        print(f"❌ Workflow generation failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def test_project_workflow_generation_with_default_config(project_id):
    """Test workflow generation with workflow_id"""
    print(f"\n=== Testing Workflow Generation with Default Config for {project_id} ===")
    
    generation_request = {
        "workflow_id": project_id  # Using workflow_id for server
    }
    
    print(f"🚀 Generating workflow with default config...")
    print(f"   Using workflow_id: {project_id}")
    print(f"   Getting task_info from setup phase")
    
    response = requests.post('http://localhost:8001/workflow/generate', json=generation_request)
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"✅ Workflow generated with default config!")
        print(f"   Status: {result.get('status', 'unknown')}")
        print(f"   Generation successful: {result.get('status') == 'success'}")
        
        return result
    else:
        print(f"❌ Workflow generation failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def test_list_projects():
    """Test listing all projects"""
    print(f"\n=== Testing Project Listing ===")
    
    response = requests.get('http://localhost:8001/projects')
    
    if response.status_code == 200:
        projects = response.json()
        
        print(f"✅ Projects retrieved:")
        print(f"\n📄 FULL PROJECTS LIST RESPONSE:")
        print(json.dumps(projects, indent=2))
        
        return projects
    else:
        print(f"❌ Failed to list projects: {response.status_code}")
        print(f"   Error: {response.text}")
        return None
    
def test_invalid_project():
    """Test behavior with invalid workflow ID"""
    print(f"\n=== Testing Invalid Workflow Handling ===")
    
    invalid_workflow_id = "invalid-workflow-123"
    
    # Test invalid workflow status
    response = requests.get(f'http://localhost:8001/workflow/{invalid_workflow_id}/status')
    print(f"Status check for invalid workflow: {response.status_code}")
    
    # Test workflow generation for invalid workflow
    generation_request = {
        "workflow_id": invalid_workflow_id
    }
    
    response = requests.post('http://localhost:8001/workflow/generate', json=generation_request)
    print(f"Workflow generation for invalid workflow: {response.status_code}")
    
    if response.status_code >= 400:
        print(f"✅ Proper error handling for invalid workflow")
        return True
    else:
        print(f"⚠️  Unexpected response: {response.text}")
        return False

def test_project_workflow_execution(project_id):
    """
    Test workflow execution for Gaokao score estimation
    Updated to use workflow_id and properly include inputs
    
    Curl command:
    ```bash
    curl -X POST http://localhost:8001/workflow/execute \
      -H "Content-Type: application/json" \
      -d '{
        "workflow_id": "gaokao-estimation-001",
        "inputs": {
          "goal": "Math: 80, English: 120, Physics: 120"
        }
      }'
    ```
    """
    print(f"\n=== Testing Gaokao Score Estimation Workflow Execution for {project_id} ===")
    
    execution_request = {
        "workflow_id": project_id,  # Using workflow_id for server
        "inputs": {
            "goal": "Math: 80, English: 120, Physics: 120"
        }
    }
    
    print(f"🚀 Executing Gaokao score estimation workflow...")
    print(f"   Workflow ID: {project_id}")
    print(f"   Input Scores: Math: 80, English: 120, Physics: 120")
    print(f"   Input keys: {list(execution_request['inputs'].keys())}")
    print(f"   Using workflow_graph from generation phase")
    
    response = requests.post('http://localhost:8001/workflow/execute', json=execution_request)
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"✅ Gaokao score estimation completed successfully!")
        print(f"   Execution result available: {result.get('execution_result') is not None}")
        
        # Show brief summary of execution result
        exec_result = result.get('execution_result')
        if exec_result:
            print(f"   Execution result type: {type(exec_result)}")
            if isinstance(exec_result, dict) and 'message' in exec_result:
                print(f"   Result preview: {str(exec_result['message'])[:100]}...")
            elif isinstance(exec_result, str):
                print(f"   Result preview: {exec_result[:100]}...")
        
        return result
    else:
        print(f"❌ Gaokao score estimation failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None


# =============================================================================
# TEST RUNNER
# =============================================================================

if __name__ == "__main__":
    print("🚀 Starting Gaokao Score Estimation Workflow Tests (Updated Structure)...")
    
    test_health_check()
    
    # Phase 1: Setup - Create workflow and generate task_info
    setup_result = test_project_setup()
    if not setup_result:
        print("❌ Workflow setup failed, stopping test")
        raise Exception("Workflow setup failed")
    
    workflow_id = setup_result['workflow_id']
    print(f"\n📋 Using workflow_id: {workflow_id}")
    
    # Check status after setup
    test_project_status(workflow_id)
    
    # Phase 2: Generation - Generate workflow graph from task_info
    workflow_result = test_project_workflow_generation(workflow_id)
    if not workflow_result:
        print("❌ Workflow generation failed, stopping test")
        raise Exception("Workflow generation failed")
    
    # Check status after generation
    test_project_status(workflow_id)
    
    # Phase 3: Execution - Execute workflow with inputs
    execution_result = test_project_workflow_execution(workflow_id)
    if not execution_result:
        print("❌ Workflow execution failed")
    else:
        print("✅ All three phases completed successfully!")
    
    # Final status check
    test_project_status(workflow_id)
    
    print("\n🏁 Gaokao score estimation workflow test execution completed.") 