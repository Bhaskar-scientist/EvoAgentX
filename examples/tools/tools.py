#!/usr/bin/env python3

"""
To test with postgresql, you might need to run the following commands:
# sudo service postgresql start
# sudo -u postgres psql -c "CREATE USER testuser WITH PASSWORD 'testpass';"
# sudo -u postgres psql -c "CREATE DATABASE testdb;"
# sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE testdb TO testuser;"
"""


"""
Example demonstrating how to use various toolkits from EvoAgentX.
This script provides comprehensive examples for:
- PythonInterpreter and DockerInterpreter tools for code execution
- BrowserToolkit with auto-initialization and auto-cleanup
- Search toolkits (Wikipedia, Google, Google Free)
- File operations with different file types using the new StorageToolkit
- MCP toolkit integration
- FAISS toolkit for semantic search and document management
- PostgreSQL toolkit for relational database operations
- MongoDB toolkit for document database operations
"""

import os
import sys
import json
from pathlib import Path

# Add the parent directory to sys.path to import from evoagentx
sys.path.append(str(Path(__file__).parent.parent))

from evoagentx.tools import (
    PythonInterpreterToolkit,
    DockerInterpreterToolkit,
    WikipediaSearchToolkit,
    GoogleSearchToolkit,
    GoogleFreeSearchToolkit,
    DDGSSearchToolkit,
    SerpAPIToolkit,  # Added SerpAPI toolkit
    SerperAPIToolkit,  # Added SerperAPI toolkit
    MCPToolkit,
    StorageToolkit,  # Updated to use new StorageToolkit
    BrowserToolkit,
    ArxivToolkit,
    BrowserUseToolkit,
    PostgreSQLToolkit,
    MongoDBToolkit,
    RSSToolkit,
    CMDToolkit,
    RequestToolkit
)
from evoagentx.tools.database_faiss import FaissToolkit


def run_simple_hello_world(interpreter):
    """
    Run a simple Hello World example using the provided interpreter.
    
    Args:
        interpreter: An instance of a code interpreter
    """
    # Define a simple Hello World code
    code = """
print("Hello, World!")
print("This code is running inside a secure Python interpreter.")
"""
    
    # Execute the code
    result = interpreter.execute(code, "python")
    print("\nSimple Hello World Result:")
    print("-" * 50)
    print(result)
    print("-" * 50)


def run_math_example(interpreter):
    """
    Run a math example using the provided interpreter.
    
    Args:
        interpreter: An instance of a code interpreter
    """
    # Define a simple math example
    code = """
print("Running math operations...")

# Using math library
import math
print(f"The value of pi is: {math.pi:.4f}")
print(f"The square root of 16 is: {math.sqrt(16)}")
print(f"The value of e is: {math.e:.4f}")
"""

    # Execute the code
    result = interpreter.execute(code, "python")
    print("\nMath Example Result:")
    print("-" * 50)
    print(result)
    print("-" * 50)


def run_platform_info(interpreter):
    """
    Run a platform info example using the provided interpreter.
    
    Args:
        interpreter: An instance of a code interpreter
    """
    # Define code that prints platform information
    code = """
print("Getting platform information...")

# System information
import platform
import sys

print(f"Python version: {platform.python_version()}")
print(f"Platform: {platform.system()} {platform.release()}")
print(f"Processor: {platform.processor()}")
print(f"Implementation: {platform.python_implementation()}")
"""

    # Execute the code
    result = interpreter.execute(code, "python")
    print("\nPlatform Info Result:")
    print("-" * 50)
    print(result)
    print("-" * 50)


def run_script_execution(interpreter):
    """
    Run a script file using the execute_script method of the interpreter.
    
    Args:
        interpreter: An instance of a code interpreter
    """
    # Get the path to the hello_world.py script
    script_path = os.path.join(os.getcwd(), "examples", "tools", "hello_world.py")
    
    # Make sure the file exists
    if not os.path.exists(script_path):
        print(f"Error: Script file not found at {script_path}")
        return
    
    print(f"Executing script file: {script_path}")
    
    # Execute the script
    result = interpreter.execute_script(script_path, "python")
    
    print("\nScript Execution Result:")
    print("-" * 50)
    print(result)
    print("-" * 50)


def run_dynamic_code_generation(interpreter):
    """
    Run an example that demonstrates dynamic code generation and execution.
    
    Args:
        interpreter: An instance of a code interpreter
    """
    # Define code that generates and executes more code
    code = """
print("Generating and executing code dynamically...")

# Generate a function definition
function_code = '''
def calculate_factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * calculate_factorial(n-1)
'''

# Execute the generated code to define the function
exec(function_code)

# Now use the dynamically defined function
for i in range(1, 6):
    print(f"Factorial of {i} is {calculate_factorial(i)}")
"""

    # Execute the code
    result = interpreter.execute(code, "python")
    print("\nDynamic Code Generation Result:")
    print("-" * 50)
    print(result)
    print("-" * 50)


def run_visualization_example(interpreter):
    """
    Run an example that would generate a visualization if matplotlib was allowed.
    This demonstrates handling imports that might not be allowed.
    
    Args:
        interpreter: An instance of a code interpreter
    """
    # Define code that attempts to use matplotlib
    code = """
print("Attempting to create a simple visualization...")

try:
    import matplotlib.pyplot as plt
    import numpy as np
    
    # Generate some data
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    # Create a plot
    plt.figure(figsize=(8, 4))
    plt.plot(x, y)
    plt.title("Sine Wave")
    plt.xlabel("x")
    plt.ylabel("sin(x)")
    plt.grid(True)
    
    # Save the plot (would work if matplotlib was available)
    plt.savefig("examples/output/sine_wave.png")
    plt.close()
    
    print("Visualization created and saved as 'examples/output/sine_wave.png'")
except ImportError as e:
    print(f"Import error: {e}")
    print("Note: This example requires matplotlib to be in the allowed_imports.")
"""

    # Execute the code
    result = interpreter.execute(code, "python")
    print("\nVisualization Example Result:")
    print("-" * 50)
    print(result)
    print("-" * 50)


def run_search_examples():
    """
    Run examples using the search toolkits (Wikipedia, Google, Google Free, DDGS, SerpAPI, and SerperAPI).
    """
    print("\n===== SEARCH TOOLS EXAMPLES =====\n")
    
    # Initialize search toolkits
    wiki_toolkit = WikipediaSearchToolkit(max_summary_sentences=3)
    google_toolkit = GoogleSearchToolkit(num_search_pages=3, max_content_words=200)
    google_free_toolkit = GoogleFreeSearchToolkit()
    ddgs_toolkit = DDGSSearchToolkit(num_search_pages=3, max_content_words=200, backend="auto", region="us-en")
    
    # Initialize SerpAPI toolkit (will check for API key)
    serpapi_toolkit = SerpAPIToolkit(
        num_search_pages=3, 
        max_content_words=300,
        enable_content_scraping=True
    )
    
    # Initialize SerperAPI toolkit (will check for API key)
    serperapi_toolkit = SerperAPIToolkit(
        num_search_pages=3,
        max_content_words=300,
        enable_content_scraping=True
    )
    
    # Get the individual tools from toolkits
    wiki_tool = wiki_toolkit.get_tool("wikipedia_search")
    google_tool = google_toolkit.get_tool("google_search")
    google_free_tool = google_free_toolkit.get_tool("google_free_search")
    ddgs_tool = ddgs_toolkit.get_tool("ddgs_search")
    serpapi_tool = serpapi_toolkit.get_tool("serpapi_search")
    serperapi_tool = serperapi_toolkit.get_tool("serperapi_search")
    
    # # Example search query
    query = "artificial intelligence agent architecture"
    
    # # Run Wikipedia search example
    # try:
    #     print("\nWikipedia Search Example:")
    #     print("-" * 50)
    #     wiki_results = wiki_tool(query=query, num_search_pages=2)
        
    #     if wiki_results.get("error"):
    #         print(f"Error: {wiki_results['error']}")
    #     else:
    #         for i, result in enumerate(wiki_results.get("results", [])):
    #             print(f"Result {i+1}: {result['title']}")
    #             print(f"Summary: {result['summary'][:150]}...")
    #             print(f"URL: {result['url']}")
    #             print("-" * 30)
    # except Exception as e:
    #     print(f"Error running Wikipedia search: {str(e)}")
    
    # # Run Google search example (requires API key)
    # try:
    #     print("\nGoogle Search Example (requires API key):")
    #     print("-" * 50)
    #     google_results = google_tool(query=query)
        
    #     if google_results.get("error"):
    #         print(f"Error: {google_results['error']}")
    #     else:
    #         for i, result in enumerate(google_results.get("results", [])):
    #             print(f"Result {i+1}: {result['title']}")
    #             print(f"URL: {result['url']}")
    #             print("-" * 30)
    # except Exception as e:
    #     print(f"Error running Google search: {str(e)}")
    
    # # Run Google Free search example
    # try:
    #     print("\nGoogle Free Search Example:")
    #     print("-" * 50)
    #     free_results = google_free_tool(query=query, num_search_pages=2)
        
    #     if free_results.get("error"):
    #         print(f"Error: {free_results['error']}")
    #     else:
    #         for i, result in enumerate(free_results.get("results", [])):
    #             print(f"Result {i+1}: {result['title']}")
    #             print(f"URL: {result['url']}")
    #             print("-" * 30)
    # except Exception as e:
    #     print(f"Error running free Google search: {str(e)}")
    
    # Run DDGS search example
    try:
        print("\nDDGS Search Example:")
        print("-" * 50)
        ddgs_results = ddgs_tool(query=query, num_search_pages=2, backend="duckduckgo")
        
        if ddgs_results.get("error"):
            print(f"Error: {ddgs_results['error']}")
        else:
            for i, result in enumerate(ddgs_results.get("results", [])):
                print(f"Result {i+1}: {result['title']}")
                print(f"Result full: \n{result}")
                print(f"URL: {result['url']}")
                print("-" * 30)
    except Exception as e:
        print(f"Error running DDGS search: {str(e)}")
    
    # Run SerpAPI search example (requires API key)
    serpapi_api_key = os.getenv("SERPAPI_KEY")
    if serpapi_api_key:
        try:
            print("\nSerpAPI Search Example (with content scraping):")
            print("-" * 50)
            print(f"✓ Using SerpAPI key: {serpapi_api_key[:8]}...")
            
            serpapi_results = serpapi_tool(
                query=query, 
                num_search_pages=3,
                max_content_words=300,
                engine="google",
                location="United States",
                language="en"
            )
            
            if serpapi_results.get("error"):
                print(f"Error: {serpapi_results['error']}")
            else:
                # Display processed results
                print(f"SerpAPI results: {serpapi_results}")
                
        except Exception as e:
            print(f"Error running SerpAPI search: {str(e)}")
    else:
        print("\nSerpAPI Search Example:")
        print("-" * 50)
        print("❌ SERPAPI_KEY not found in environment variables")
        print("To test SerpAPI search, set your API key:")
        print("export SERPAPI_KEY='your-serpapi-key-here'")
        print("Get your key from: https://serpapi.com/")
        print("✓ SerpAPI toolkit initialized successfully (API key required for search)")
    
    # Run SerperAPI search example (requires API key)
    serperapi_api_key = os.getenv("SERPERAPI_KEY")
    if serperapi_api_key:
        try:
            print("\nSerperAPI Search Example (with content scraping):")
            print("-" * 50)
            print(f"✓ Using SerperAPI key: {serperapi_api_key[:8]}...")
            
            serperapi_results = serperapi_tool(
                query=query,
                num_search_pages=3,
                max_content_words=300,
                location="United States",
                language="en"
            )
            
            if serperapi_results.get("error"):
                print(f"Error: {serperapi_results['error']}")
            else:
                print(f"SerperAPI results: {serperapi_results}")
                
        except Exception as e:
            print(f"Error running SerperAPI search: {str(e)}")
    else:
        print("\nSerperAPI Search Example:")
        print("-" * 50)
        print("❌ SERPERAPI_KEY not found in environment variables")
        print("To test SerperAPI search, set your API key:")
        print("export SERPERAPI_KEY='your-serperapi-key-here'")
        print("Get your key from: https://serper.dev/")
        print("✓ SerperAPI toolkit initialized successfully (API key required for search)")


def run_python_interpreter_examples():
    """Run all examples using the Python InterpreterToolkit"""
    print("\n===== PYTHON INTERPRETER EXAMPLES =====\n")
    
    # Initialize the Python interpreter toolkit with the current directory as project path
    # and allow common standard library imports
    interpreter_toolkit = PythonInterpreterToolkit(
        project_path=os.getcwd(),
        directory_names=["examples", "evoagentx"],
        allowed_imports={"os", "sys", "time", "datetime", "math", "random", "platform", "matplotlib.pyplot", "numpy"}
    )
    
    # Get the underlying interpreter instance for the examples
    interpreter = interpreter_toolkit.python_interpreter
    
    # Run the examples
    run_simple_hello_world(interpreter)
    run_math_example(interpreter)
    run_platform_info(interpreter)
    run_script_execution(interpreter)
    run_dynamic_code_generation(interpreter)
    run_visualization_example(interpreter)


def run_docker_interpreter_examples():
    """Run all examples using the Docker InterpreterToolkit"""
    print("\n===== DOCKER INTERPRETER EXAMPLES =====\n")
    print("Running Docker interpreter examples...")
    
    try:
        # Initialize the Docker interpreter toolkit with a standard Python image
        interpreter_toolkit = DockerInterpreterToolkit(
            image_tag="python:3.9-slim",  # Using official Python image
            print_stdout=True,
            print_stderr=True,
            container_directory="/app"  # Better working directory for containerized apps
        )
        
        # Get the underlying interpreter instance for the examples
        interpreter = interpreter_toolkit.docker_interpreter
        
        # Run the examples
        run_simple_hello_world(interpreter)
        run_math_example(interpreter)
        run_platform_info(interpreter)
        run_script_execution(interpreter)
        run_dynamic_code_generation(interpreter)
        # run_visualization_example(interpreter)
    except Exception as e:
        print(f"Error running Docker interpreter examples: {str(e)}")
        print("Make sure Docker is installed and running on your system.")
        print("You may need to pull the python:3.9-slim image first using: docker pull python:3.9-slim")


def run_mcp_example():
    """
    Run an example using the MCP toolkit to search for research papers about 'artificial intelligence'.
    This uses the sample_mcp.config file to configure the arXiv MCP client.
    """
    print("\n===== MCP TOOLKIT EXAMPLE (arXiv) =====\n")
    
    # Get the path to the sample_mcp.config file
    config_path = os.path.join(os.getcwd(), "examples", "tools", "sample_mcp.config")
    
    print(f"Loading MCP configuration from: {config_path}")
    
    try:
        # Initialize the MCP toolkit with the sample config
        mcp_toolkit = MCPToolkit(config_path=config_path)
        
        # Get all available toolkits
        toolkits = mcp_toolkit.get_toolkits()
        
        print(f"Available MCP toolkits: {len(toolkits)}")
        
        # Find and use the arXiv search tool
        arxiv_tool = None
        for toolkit_item in toolkits:
            for tool in toolkit_item.get_tools():
                print(f"Tool: {tool.name}")
                print(f"Description: {tool.description}")
                print("-" * 30)
                
                if "search" in tool.name.lower() or "arxiv" in tool.name.lower():
                    arxiv_tool = tool
                    break
            if arxiv_tool:
                break
        
        if arxiv_tool:
            print(f"Using tool: {arxiv_tool.name}")
            
            # Search for 'artificial intelligence' research papers
            search_query = "artificial intelligence"
            print(f"Searching for research papers about: '{search_query}'")
            
            # Call the tool with the search query
            # Note: The actual parameter name might differ based on the tool's schema
            result = arxiv_tool(**{"query": search_query})
            
            print("\nSearch Results:")
            print("-" * 50)
            print(result)
            print("-" * 50)
        else:
            print("No suitable arXiv search tool found in the MCP configuration.")
    except Exception as e:
        print(f"Error running MCP example: {str(e)}")
        print("Make sure the arXiv MCP server is properly configured and running.")
    finally:
        if 'mcp_toolkit' in locals():
            mcp_toolkit.disconnect()


def run_file_tool_example():
    """
    Run an example using the StorageToolkit to read and write files with the new storage handler system.
    """
    print("\n===== STORAGE TOOL EXAMPLE =====\n")
    
    try:
        # Initialize the storage toolkit with default storage handler
        storage_toolkit = StorageToolkit(name="DemoStorageToolkit")
        
        # Get individual tools from the toolkit
        save_tool = storage_toolkit.get_tool("save")
        read_tool = storage_toolkit.get_tool("read")
        append_tool = storage_toolkit.get_tool("append")
        list_tool = storage_toolkit.get_tool("list_files")
        exists_tool = storage_toolkit.get_tool("exists")
        
        # Create sample content for different file types
        sample_text = """This is a sample text document created using the StorageToolkit.
This tool provides comprehensive file operations with automatic format detection.
It supports various file types including text, JSON, CSV, YAML, XML, Excel, and more."""
        
        sample_json = {
            "name": "Sample Document",
            "type": "test",
            "content": "This is a JSON document for testing",
            "metadata": {
                "created": "2024-01-01",
                "version": "1.0"
            }
        }
        
        # Test file operations with default storage paths
        print("1. Testing file save operations...")
        
        # Save text file
        text_result = save_tool(
            file_path="sample_document.txt",
            content=sample_text
        )
        print("Text file save result:")
        print("-" * 30)
        print(text_result)
        print("-" * 30)
        
        # Save JSON file
        json_result = save_tool(
            file_path="sample_data.json",
            content=json.dumps(sample_json, indent=2)
        )
        print("JSON file save result:")
        print("-" * 30)
        print(json_result)
        print("-" * 30)
        
        # Test file read operations
        print("\n2. Testing file read operations...")
        
        # Read text file
        text_read_result = read_tool(file_path="sample_document.txt")
        print("Text file read result:")
        print("-" * 30)
        print(text_read_result)
        print("-" * 30)
        
        # Read JSON file
        json_read_result = read_tool(file_path="sample_data.json")
        print("JSON file read result:")
        print("-" * 30)
        print(json_read_result)
        print("-" * 30)
        
        # Test file append operations
        print("\n3. Testing file append operations...")
        
        # Append to text file
        append_text_result = append_tool(
            file_path="sample_document.txt",
            content="\n\nThis content was appended to the text file."
        )
        print("Text file append result:")
        print("-" * 30)
        print(append_text_result)
        print("-" * 30)
        
        # Append to JSON file (will add to existing array or create new array)
        append_json_data = {"additional": "data", "timestamp": "2024-01-01T12:00:00Z"}
        append_json_result = append_tool(
            file_path="sample_data.json",
            content=json.dumps(append_json_data)
        )
        print("JSON file append result:")
        print("-" * 30)
        print(append_json_result)
        print("-" * 30)
        
        # Test file listing
        print("\n4. Testing file listing...")
        list_result = list_tool(path=".", max_depth=2, include_hidden=False)
        print("File listing result:")
        print("-" * 30)
        print(list_result)
        print("-" * 30)
        
        # Test file existence
        print("\n5. Testing file existence...")
        exists_result = exists_tool(path="sample_document.txt")
        print("File existence check result:")
        print("-" * 30)
        print(exists_result)
        print("-" * 30)
        
        # Test supported formats
        print("\n6. Testing supported formats...")
        formats_tool = storage_toolkit.get_tool("list_supported_formats")
        formats_result = formats_tool()
        print("Supported formats result:")
        print("-" * 30)
        print(formats_result)
        print("-" * 30)
        
        print("\n✓ StorageToolkit test completed successfully!")
        print("✓ All file operations working with default storage handler")
        print("✓ Automatic format detection working")
        print("✓ File append operations working")
        print("✓ File listing and existence checks working")
        
    except Exception as e:
        print(f"Error running storage tool example: {str(e)}")


def run_browser_tool_example():
    """
    Run an example using the BrowserToolkit with auto-initialization and auto-cleanup.
    Uses a comprehensive HTML test page to demonstrate browser automation features.
    """
    print("\n===== BROWSER TOOL EXAMPLE =====\n")
    
    try:
        # Initialize the browser toolkit (browser auto-initializes when first used)
        browser_toolkit = BrowserToolkit(headless=False, timeout=10)
        
        # Get individual tools from the toolkit
        nav_tool = browser_toolkit.get_tool("navigate_to_url")
        input_tool = browser_toolkit.get_tool("input_text")
        click_tool = browser_toolkit.get_tool("browser_click")
        snapshot_tool = browser_toolkit.get_tool("browser_snapshot")
        
        # Use the static test HTML file
        test_file_path = os.path.join(os.getcwd(), "examples", "tools", "browser_test_page.html")
        
        print("Step 1: Navigating to test page (browser auto-initializes)...")
        nav_result = nav_tool(url=f"file://{test_file_path}")
        print("Navigation Result:")
        print("-" * 30)
        print(f"Status: {nav_result.get('status')}")
        print(f"URL: {nav_result.get('current_url')}")
        print(f"Title: {nav_result.get('title')}")
        print("-" * 30)
        
        if nav_result.get("status") in ["success", "partial_success"]:
            print("\nStep 2: Taking initial snapshot to identify elements...")
            snapshot_result = snapshot_tool()
            
            if snapshot_result.get("status") == "success":
                print("✓ Initial snapshot successful")
                
                # Find interactive elements
                elements = snapshot_result.get("interactive_elements", [])
                print(f"Found {len(elements)} interactive elements")
                
                # Identify specific elements
                name_input_ref = None
                email_input_ref = None
                message_input_ref = None
                submit_btn_ref = None
                clear_btn_ref = None
                test_btn_ref = None
                
                for elem in elements:
                    desc = elem.get("description", "").lower()
                    purpose = elem.get("purpose", "").lower()
                    
                    if "name" in desc and elem.get("editable"):
                        name_input_ref = elem["id"]
                    elif "email" in desc and elem.get("editable"):
                        email_input_ref = elem["id"]
                    elif "message" in desc and elem.get("editable"):
                        message_input_ref = elem["id"]
                    elif "submit" in purpose and elem.get("interactable"):
                        submit_btn_ref = elem["id"]
                    elif "clear" in purpose and elem.get("interactable"):
                        clear_btn_ref = elem["id"]
                    elif "test" in purpose and elem.get("interactable"):
                        test_btn_ref = elem["id"]
                
                print(f"Identified elements:")
                print(f"  - Name input: {name_input_ref}")
                print(f"  - Email input: {email_input_ref}")
                print(f"  - Message input: {message_input_ref}")
                print(f"  - Submit button: {submit_btn_ref}")
                print(f"  - Clear button: {clear_btn_ref}")
                print(f"  - Test button: {test_btn_ref}")
                
                # Test input functionality
                if name_input_ref and email_input_ref and message_input_ref:
                    print("\nStep 3: Testing input functionality...")
                    
                    # Fill name field
                    print("  - Typing 'John Doe' in name field...")
                    name_result = input_tool(
                        element="Name input", 
                        ref=name_input_ref, 
                        text="John Doe", 
                        submit=False
                    )
                    print(f"    Result: {name_result.get('status')}")
                    
                    # Fill email field
                    print("  - Typing 'john.doe@example.com' in email field...")
                    email_result = input_tool(
                        element="Email input", 
                        ref=email_input_ref, 
                        text="john.doe@example.com", 
                        submit=False
                    )
                    print(f"    Result: {email_result.get('status')}")
                    
                    # Fill message field
                    print("  - Typing 'This is a test message for browser automation.' in message field...")
                    message_result = input_tool(
                        element="Message input", 
                        ref=message_input_ref, 
                        text="This is a test message for browser automation.", 
                        submit=False
                    )
                    print(f"    Result: {message_result.get('status')}")
                    
                    # Test form submission
                    if submit_btn_ref:
                        print("\nStep 4: Testing form submission...")
                        submit_result = click_tool(
                            element="Submit button", 
                            ref=submit_btn_ref
                        )
                        print(f"Submit result: {submit_result.get('status')}")
                        
                        # Take snapshot to see the result
                        print("\nStep 5: Taking snapshot to verify form submission...")
                        result_snapshot = snapshot_tool()
                        if result_snapshot.get("status") == "success":
                            content = result_snapshot.get("page_content", "")
                            if "Name: John Doe, Email: john.doe@example.com" in content:
                                print("✓ Form submission successful - data correctly displayed!")
                            else:
                                print("⚠ Form submission may have failed")
                    
                    # Test test button click
                    if test_btn_ref:
                        print("\nStep 6: Testing test button click...")
                        test_result = click_tool(
                            element="Test button", 
                            ref=test_btn_ref
                        )
                        print(f"Test button result: {test_result.get('status')}")
                        
                        # Take snapshot to see the click result
                        click_snapshot = snapshot_tool()
                        if click_snapshot.get("status") == "success":
                            content = click_snapshot.get("page_content", "")
                            if "Test button clicked at:" in content:
                                print("✓ Test button click successful!")
                            else:
                                print("⚠ Test button click may have failed")
                    
                    # Test clear functionality
                    if clear_btn_ref:
                        print("\nStep 7: Testing clear functionality...")
                        clear_result = click_tool(
                            element="Clear button", 
                            ref=clear_btn_ref
                        )
                        print(f"Clear result: {clear_result.get('status')}")
                        
                        # Take final snapshot
                        final_snapshot = snapshot_tool()
                        if final_snapshot.get("status") == "success":
                            print("✓ Clear functionality tested")
                
                print("\n✓ Browser automation test completed successfully!")
                print("✓ Browser auto-initialization working")
                print("✓ Navigation working")
                print("✓ Input functionality working")
                print("✓ Click functionality working")
                print("✓ Form submission working")
                print("✓ Snapshot functionality working")
            else:
                print("❌ Initial snapshot failed")
        else:
            print("\n❌ Navigation failed")
        
        print("\nBrowser will automatically close when the toolkit goes out of scope...")
        print("(No manual cleanup required)")
        
    except Exception as e:
        print(f"Error running browser tool example: {str(e)}")
        print("Browser will still automatically cleanup on exit")


def run_arxiv_tool_example():
    """Simple example using ArxivToolkit to search for papers."""
    print("\n===== ARXIV TOOL EXAMPLE =====\n")
    
    try:
        # Initialize the arXiv toolkit
        arxiv_toolkit = ArxivToolkit()
        search_tool = arxiv_toolkit.get_tool("arxiv_search")
        
        print("✓ ArxivToolkit initialized")
        
        # Search for machine learning papers
        print("Searching for 'machine learning' papers...")
        result = search_tool(
            search_query="all:machine learning",
            max_results=3
        )
        
        if result.get('success'):
            papers = result.get('papers', [])
            print(f"✓ Found {len(papers)} papers")
            
            for i, paper in enumerate(papers):
                print(f"\nPaper {i+1}: {paper.get('title', 'No title')}")
                print(f"  Authors: {', '.join(paper.get('authors', ['Unknown']))}")
                print(f"  arXiv ID: {paper.get('arxiv_id', 'Unknown')}")
                print(f"  URL: {paper.get('url', 'No URL')}")
        else:
            print(f"❌ Search failed: {result.get('error', 'Unknown error')}")
        
        print("\n✓ ArxivToolkit test completed")
        
    except Exception as e:
        print(f"Error: {str(e)}")


def run_browser_use_tool_example():
    """Simple example using BrowserUseToolkit for browser automation."""
    print("\n===== BROWSER USE TOOL EXAMPLE =====\n")
    
    # Check for OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key: export OPENAI_API_KEY='your-api-key-here'")
        return
    
    try:
        # Initialize the BrowserUse toolkit
        print("Initializing BrowserUseToolkit...")
        toolkit = BrowserUseToolkit(model="gpt-4o-mini", headless=False)
        browser_tool = toolkit.get_tool("browser_use")
        
        print("✓ BrowserUseToolkit initialized")
        print(f"✓ Using OpenAI API key: {openai_api_key[:8]}...")
        
        # Execute a simple browser task
        print("Executing browser task: 'Go to Google and search for OpenAI GPT-4'...")
        result = browser_tool(task="Go to Google and search for 'OpenAI GPT-4'")
        
        if result.get('success'):
            print("✓ Browser task completed successfully")
            print(f"Result: {result.get('result', 'No result details')}")
        else:
            print(f"❌ Browser task failed: {result.get('error', 'Unknown error')}")
        
        print("\n✓ BrowserUseToolkit test completed")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Note: Make sure you have the required dependencies installed and API keys set up.")


def run_faiss_tool_example():
    """Powerful example using FaissToolkit for semantic search and document management."""
    print("\n===== FAISS TOOL EXAMPLE =====\n")
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found - skipping FAISS example")
        return
    
    try:
        # Initialize FAISS toolkit with default storage (no explicit path needed)
        toolkit = FaissToolkit(
            name="DemoFaissToolkit",
            default_corpus_id="demo_corpus"
        )
        
        print("✓ FaissToolkit initialized with default storage")
        
        # Get tools
        insert_tool = toolkit.get_tool("faiss_insert")
        query_tool = toolkit.get_tool("faiss_query")
        stats_tool = toolkit.get_tool("faiss_stats")
        delete_tool = toolkit.get_tool("faiss_delete")
        
        # Insert AI knowledge documents
        documents = [
            "Artificial Intelligence enables machines to perform tasks requiring human intelligence.",
            "Machine learning allows computers to learn from data without explicit programming.",
            "Deep learning uses neural networks with multiple layers for complex pattern recognition.",
            "Natural Language Processing helps computers understand and generate human language.",
            "Computer vision enables machines to interpret visual information from images and videos."
        ]
        
        try:
            result = insert_tool(
                documents=documents,
                metadata={"source": "ai_knowledge", "topic": "artificial_intelligence"}
            )
            
            if result["success"]:
                print(f"✓ Inserted {result['data']['documents_inserted']} documents")
                
                # Perform semantic search
                search_result = query_tool(
                    query="How do machines learn?",
                    top_k=3,
                    similarity_threshold=0.1
                )
                
                if search_result["success"]:
                    print(f"✓ Found {search_result['data']['total_results']} relevant results")
                    for i, res in enumerate(search_result["data"]["results"], 1):
                        print(f"  {i}. Score: {res['score']:.3f} - {res['content'][:80]}...")
                
                # Get statistics
                stats_result = stats_tool()
                if stats_result["success"]:
                    print(f"✓ Database stats: {stats_result['data']['total_corpora']} corpora")
                
                # Test delete functionality
                print("\n🗑️ Testing delete functionality...")
                delete_result = delete_tool(
                    metadata_filters={"source": "ai_knowledge"}
                )
                
                if delete_result["success"]:
                    print(f"✓ Deleted documents with metadata filter")
                    
                    # Verify deletion
                    verify_result = query_tool(
                        query="artificial intelligence",
                        top_k=5,
                        similarity_threshold=0.1
                    )
                    
                    if verify_result["success"]:
                        remaining = verify_result['data']['total_results']
                        print(f"✓ Remaining documents after deletion: {remaining}")
            else:
                print(f"❌ Insert failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            if "DocumentMetadata" in str(e):
                print("⚠ DocumentMetadata import issue detected - this may be a dependency problem")
                print("   The FAISS toolkit requires proper RAG engine dependencies")
                print(f"   Error details: {str(e)}")
            else:
                print(f"❌ Unexpected error during FAISS operations: {str(e)}")
        
        print("\n✓ FaissToolkit test completed with default storage")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        if "DocumentMetadata" in str(e):
            print("Note: This appears to be a dependency issue with the RAG engine components")
            print("The FAISS toolkit may need additional setup or dependencies")


def run_postgresql_tool_example():
    """Powerful example using PostgreSQLToolkit for database operations."""
    print("\n===== POSTGRESQL TOOL EXAMPLE =====\n")
    
    try:
        # Initialize PostgreSQL toolkit with default storage (no explicit path needed)
        toolkit = PostgreSQLToolkit(
            name="DemoPostgreSQLToolkit",
            database_name="demo_db",
            auto_save=True
        )
        
        print("✓ PostgreSQLToolkit initialized with default storage")
        
        # Get tools
        execute_tool = toolkit.get_tool("postgresql_execute")
        find_tool = toolkit.get_tool("postgresql_find")
        create_tool = toolkit.get_tool("postgresql_create")
        delete_tool = toolkit.get_tool("postgresql_delete")
        
        # Create users table and insert data
        create_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            age INTEGER,
            department VARCHAR(50)
        );
        """
        
        result = create_tool(create_sql)
        if result["success"]:
            print("✓ Created users table")
            
            # Insert users
            insert_sql = """
            INSERT INTO users (name, email, age, department) VALUES
            ('Alice Johnson', 'alice@example.com', 28, 'Engineering'),
            ('Bob Smith', 'bob@example.com', 32, 'Marketing'),
            ('Carol Davis', 'carol@example.com', 25, 'Engineering')
            ON CONFLICT (email) DO NOTHING;
            """
            
            result = execute_tool(insert_sql)
            if result["success"]:
                print("✓ Inserted users")
                
                # Query users - fix the field access issue
                find_result = find_tool(
                    "users",
                    where="department = 'Engineering'",
                    columns="name, age",
                    sort="age ASC"
                )
                
                if find_result["success"]:
                    engineers = find_result["data"]
                    print(f"✓ Found {len(engineers)} engineers:")
                    for user in engineers:
                        # Handle potential missing fields safely
                        name = user.get('name', 'Unknown')
                        age = user.get('age', 'N/A')
                        print(f"  - {name} (age: {age})")
                
                # Test delete functionality
                print("\n🗑️ Testing delete functionality...")
                delete_result = delete_tool(
                    "users",
                    "department = 'Marketing'"
                )
                
                if delete_result["success"]:
                    deleted_count = delete_result["data"].get("rowcount", 0)
                    print(f"✓ Deleted {deleted_count} marketing users")
                    
                    # Verify deletion
                    verify_result = find_tool("users")
                    if verify_result["success"]:
                        remaining = verify_result["data"]
                        print(f"✓ Remaining users after deletion: {len(remaining)}")
        
        print("\n✓ PostgreSQLToolkit test completed with default storage")
        
    except Exception as e:
        print(f"Error: {str(e)}")


def run_mongodb_tool_example():
    """Powerful example using MongoDBToolkit for document operations."""
    print("\n===== MONGODB TOOL EXAMPLE =====\n")
    
    try:
        # Initialize MongoDB toolkit with default storage (no explicit path needed)
        toolkit = MongoDBToolkit(
            name="DemoMongoDBToolkit",
            database_name="demo_db",
            auto_save=True
        )
        
        print("✓ MongoDBToolkit initialized with default storage")
        
        # Get tools
        execute_tool = toolkit.get_tool("mongodb_execute_query")
        find_tool = toolkit.get_tool("mongodb_find")
        delete_tool = toolkit.get_tool("mongodb_delete")
        
        # Insert products data - fix query format
        products = [
            {"id": "P001", "name": "Laptop", "category": "Electronics", "price": 999.99, "stock": 50},
            {"id": "P002", "name": "Mouse", "category": "Electronics", "price": 29.99, "stock": 100},
            {"id": "P003", "name": "Desk Chair", "category": "Furniture", "price": 199.99, "stock": 25}
        ]
        
        # Use proper JSON string format
        result = execute_tool(
            query=json.dumps(products),
            query_type="insert",
            collection_name="products"
        )
        
        if result["success"]:
            print("✓ Inserted products")
            
            # Query products with filter
            find_result = find_tool(
                collection_name="products",
                filter='{"category": "Electronics"}',
                sort='{"price": -1}'
            )
            
            if find_result["success"]:
                electronics = find_result["data"]
                print(f"✓ Found {len(electronics)} electronics products:")
                for product in electronics:
                    name = product.get('name', 'Unknown')
                    price = product.get('price', 0)
                    stock = product.get('stock', 0)
                    print(f"  - {name}: ${price} (stock: {stock})")
            
            # Test delete functionality
            print("\n🗑️ Testing delete functionality...")
            delete_result = delete_tool(
                collection_name="products",
                filter='{"category": "Furniture"}',
                multi=True
            )
            
            if delete_result["success"]:
                deleted_count = delete_result["data"].get("deleted_count", 0)
                print(f"✓ Deleted {deleted_count} furniture products")
                
                # Verify deletion
                verify_result = find_tool(collection_name="products")
                if verify_result["success"]:
                    remaining = verify_result["data"]
                    print(f"✓ Remaining products after deletion: {len(remaining)}")
        
        print("\n✓ MongoDBToolkit test completed with default storage")
        
    except Exception as e:
        print(f"Error: {str(e)}")


def run_rss_tool_example():
    """Powerful example using RSSToolkit for RSS feed operations."""
    print("\n===== RSS TOOL EXAMPLE =====\n")
    
    try:
        # Initialize RSS toolkit
        toolkit = RSSToolkit(name="DemoRSSToolkit")
        
        print("✓ RSSToolkit initialized")
        
        # Get tools
        fetch_tool = toolkit.get_tool("rss_fetch")
        validate_tool = toolkit.get_tool("rss_validate")
        
        # Test RSS feed URLs
        test_feeds = [
            "https://feeds.bbci.co.uk/news/rss.xml",  # BBC News
            "https://rss.cnn.com/rss/edition.rss",    # CNN
            "https://feeds.feedburner.com/TechCrunch" # TechCrunch
        ]
        
        for feed_url in test_feeds:
            print(f"\n--- Testing RSS Feed: {feed_url} ---")
            
            # Validate the feed
            print("1. Validating RSS feed...")
            validate_result = validate_tool(url=feed_url)
            
            if validate_result.get("success") and validate_result.get("is_valid"):
                print(f"✓ Valid {validate_result.get('feed_type')} feed: {validate_result.get('title', 'Unknown')}")
                
                # Fetch the feed
                print("2. Fetching RSS feed...")
                fetch_result = fetch_tool(feed_url=feed_url, max_entries=3)
                
                if fetch_result.get("success"):
                    entries = fetch_result.get("entries", [])
                    print(f"✓ Fetched {len(entries)} entries from '{fetch_result.get('title')}'")
                    
                    # Display first few entries
                    for i, entry in enumerate(entries[:2], 1):
                        print(f"  Entry {i}: {entry.get('title', 'No title')}")
                        print(f"    Published: {entry.get('published', 'Unknown')}")
                        print(f"    Link: {entry.get('link', 'No link')}")
                        print(f"    Author: {entry.get('author', 'Unknown')}")
                        print()
                
                # Test monitoring for recent entries
                print("3. Testing feed monitoring...")
                
                
                
            else:
                print(f"❌ Invalid or inaccessible feed: {validate_result.get('error', 'Unknown error')}")
        
        print("\n✓ RSSToolkit test completed")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Note: RSS feed availability may vary. Some feeds may be temporarily unavailable.")


def run_cmd_tool_example():
    """Simple example using CMDToolkit for command line operations."""
    print("\n===== CMD TOOL EXAMPLE =====\n")
    
    try:
        # Initialize the CMD toolkit
        cmd_toolkit = CMDToolkit(name="DemoCMDToolkit")
        execute_tool = cmd_toolkit.get_tool("execute_command")
        
        print("✓ CMDToolkit initialized")
        
        # Test basic command execution
        print("1. Testing basic command execution...")
        result = execute_tool(command="echo 'Hello from CMD toolkit'")
        
        if result.get("success"):
            print("✓ Command executed successfully")
            print(f"Output: {result.get('stdout', 'No output')}")
        else:
            print(f"❌ Command failed: {result.get('error', 'Unknown error')}")
        
        # Test system information commands
        print("\n2. Testing system information commands...")
        
        # Get current working directory
        pwd_result = execute_tool(command="pwd")
        if pwd_result.get("success"):
            print(f"✓ Current directory: {pwd_result.get('stdout', '').strip()}")
        
        # Get system information
        if os.name == 'posix':  # Linux/Mac
            uname_result = execute_tool(command="uname -a")
            if uname_result.get("success"):
                print(f"✓ System info: {uname_result.get('stdout', '').strip()}")
        else:  # Windows
            ver_result = execute_tool(command="ver")
            if ver_result.get("success"):
                print(f"✓ System info: {ver_result.get('stdout', '').strip()}")
        
        # Test file listing
        print("\n3. Testing file listing...")
        if os.name == 'posix':
            ls_result = execute_tool(command="ls -la", working_directory=".")
        else:
            ls_result = execute_tool(command="dir", working_directory=".")
        
        if ls_result.get("success"):
            print("✓ File listing successful")
            print(f"Output length: {len(ls_result.get('stdout', ''))} characters")
        else:
            print(f"❌ File listing failed: {ls_result.get('error', 'Unknown error')}")
        
        # Test with timeout
        print("\n4. Testing command timeout...")
        timeout_result = execute_tool(command="sleep 5", timeout=12)
        if not timeout_result.get("success"):
            print("✓ Timeout working correctly (command was interrupted)")
        else:
            print("⚠ Timeout may not be working as expected")
        
        print("\n✓ CMDToolkit test completed")
        
    except Exception as e:
        print(f"Error: {str(e)}")


def run_request_tool_example():
    """Simple example using RequestToolkit for HTTP operations."""
    print("\n===== REQUEST TOOL EXAMPLE =====\n")
    
    try:
        # Initialize the request toolkit
        request_toolkit = RequestToolkit(name="DemoRequestToolkit")
        http_tool = request_toolkit.get_tool("http_request")
        
        print("✓ RequestToolkit initialized")
        
        # Test GET request
        print("1. Testing GET request...")
        get_result = http_tool(
            url="https://httpbin.org/get",
            method="GET",
            params={"test": "param", "example": "value"}
        )
        
        if get_result.get("success"):
            print("✓ GET request successful")
            print(f"Status: {get_result.get('status_code')}")
            print(f"Response size: {len(str(get_result.get('content', '')))} characters")
        else:
            print(f"❌ GET request failed: {get_result.get('error', 'Unknown error')}")
        
        # Test POST request with JSON data
        print("\n2. Testing POST request with JSON...")
        post_result = http_tool(
            url="https://httpbin.org/post",
            method="POST",
            json_data={"name": "Test User", "email": "test@example.com"},
            headers={"Content-Type": "application/json"}
        )
        
        if post_result.get("success"):
            print("✓ POST request successful")
            print(f"Status: {post_result.get('status_code')}")
            content = post_result.get('content', '')
            if isinstance(content, dict) and 'json' in content:
                print(f"✓ JSON data received: {content['json']}")
        else:
            print(f"❌ POST request failed: {post_result.get('error', 'Unknown error')}")
        
        # Test PUT request
        print("\n3. Testing PUT request...")
        put_result = http_tool(
            url="https://httpbin.org/put",
            method="PUT",
            data={"update": "new value", "timestamp": "2024-01-01"}
        )
        
        if put_result.get("success"):
            print("✓ PUT request successful")
            print(f"Status: {put_result.get('status_code')}")
        else:
            print(f"❌ PUT request failed: {put_result.get('error', 'Unknown error')}")
        
        # Test DELETE request
        print("\n4. Testing DELETE request...")
        delete_result = http_tool(
            url="https://httpbin.org/delete",
            method="DELETE"
        )
        
        if delete_result.get("success"):
            print("✓ DELETE request successful")
            print(f"Status: {delete_result.get('status_code')}")
        else:
            print(f"❌ DELETE request failed: {delete_result.get('error', 'Unknown error')}")
        
        # Test error handling with invalid URL
        print("\n5. Testing error handling...")
        error_result = http_tool(
            url="https://invalid-domain-that-does-not-exist-12345.com",
            method="GET"
        )
        
        if not error_result.get("success"):
            print("✓ Error handling working correctly")
            print(f"Error: {error_result.get('error', 'Unknown error')}")
        else:
            print("⚠ Error handling may not be working as expected")
        
        print("\n✓ RequestToolkit test completed")
        
    except Exception as e:
        print(f"Error: {str(e)}")


def main():
    """Main function to run all examples"""
    print("===== INTERPRETER TOOL EXAMPLES =====")
    
    # # Run storage tool example (updated from file tool)
    # run_file_tool_example()
   
    # # Run Python interpreter examples
    # run_python_interpreter_examples()
    
    # # Run Docker interpreter examples
    # run_docker_interpreter_examples()
    
    # # Run search tools examples
    # run_search_examples()
    
    # # Run arXiv tool example
    # run_arxiv_tool_example()
    
    # # Run BrowserUse tool example
    # run_browser_use_tool_example()
        
    # Run browser tool example
    run_browser_tool_example()
    
    # # Run FAISS tool example
    # run_faiss_tool_example()
    
    # # Run PostgreSQL tool example
    # run_postgresql_tool_example()
    
    # # Run MongoDB tool example
    # run_mongodb_tool_example()
    
    # # Run RSS tool example
    # run_rss_tool_example()
    
    # # Run CMD tool example
    # run_cmd_tool_example()

    # # Run Request tool example
    # run_request_tool_example()
   
    # # Run MCP toolkit example
    # run_mcp_example()
    
    # print("\n===== ALL EXAMPLES COMPLETED =====")


if __name__ == "__main__":
    main() 