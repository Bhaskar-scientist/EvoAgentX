#!/usr/bin/env python3
"""
Example demonstrating how to use the PythonInterpreter and DockerInterpreter tools.
This script provides examples for running simple Python code and script files.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to sys.path to import from evoagentx
sys.path.append(str(Path(__file__).parent.parent))

from evoagentx.tools.interpreter_python import PythonInterpreter
from evoagentx.tools.interpreter_docker import DockerInterpreter
from evoagentx.tools.search_wiki import SearchWiki
from evoagentx.tools.search_google import SearchGoogle
from evoagentx.tools.search_google_f import SearchGoogleFree
from evoagentx.tools.mcp import MCPToolkit
from evoagentx.tools.file_tool import FileTool
from evoagentx.tools.browser_tool import BrowserTool


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
    script_path = os.path.join(os.getcwd(), "examples", "output", "tools", "hello_world.py")
    
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
    plt.savefig("sine_wave.png")
    plt.close()
    
    print("Visualization created and saved as 'sine_wave.png'")
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
    Run examples using the search tools (Wikipedia, Google, and Google Free).
    """
    print("\n===== SEARCH TOOLS EXAMPLES =====\n")
    
    # Initialize search tools
    wiki_search = SearchWiki(max_sentences=3)
    google_search = SearchGoogle(num_search_pages=3, max_content_words=200)
    google_free = SearchGoogleFree()
    
    # Example search query
    query = "artificial intelligence agent architecture"
    
    # Run Wikipedia search example
    try:
        print("\nWikipedia Search Example:")
        print("-" * 50)
        wiki_results = wiki_search.search(query=query, num_search_pages=2)
        
        if wiki_results.get("error"):
            print(f"Error: {wiki_results['error']}")
        else:
            for i, result in enumerate(wiki_results.get("results", [])):
                print(f"Result {i+1}: {result['title']}")
                print(f"Summary: {result['summary'][:150]}...")
                print(f"URL: {result['url']}")
                print("-" * 30)
    except Exception as e:
        print(f"Error running Wikipedia search: {str(e)}")
    
    # Run Google search example (requires API key)
    try:
        print("\nGoogle Search Example (requires API key):")
        print("-" * 50)
        google_results = google_search.search(query=query)
        
        if google_results.get("error"):
            print(f"Error: {google_results['error']}")
        else:
            for i, result in enumerate(google_results.get("results", [])):
                print(f"Result {i+1}: {result['title']}")
                print(f"URL: {result['url']}")
                print("-" * 30)
    except Exception as e:
        print(f"Error running Google search: {str(e)}")
    
    # Run Google Free search example
    try:
        print("\nGoogle Free Search Example:")
        print("-" * 50)
        free_results = google_free.search(query=query, num_search_pages=2)
        
        if free_results.get("error"):
            print(f"Error: {free_results['error']}")
        else:
            for i, result in enumerate(free_results.get("results", [])):
                print(f"Result {i+1}: {result['title']}")
                print(f"URL: {result['url']}")
                print("-" * 30)
    except Exception as e:
        print(f"Error running free Google search: {str(e)}")


def run_python_interpreter_examples():
    """Run all examples using the Python Interpreter"""
    print("\n===== PYTHON INTERPRETER EXAMPLES =====\n")
    
    # Initialize the Python interpreter with the current directory as project path
    # and allow common standard library imports
    interpreter = PythonInterpreter(
        project_path=os.getcwd(),
        directory_names=["examples", "evoagentx"],
        allowed_imports={"os", "sys", "time", "datetime", "math", "random", "platform"}
    )
    
    # Run the examples
    run_simple_hello_world(interpreter)
    run_math_example(interpreter)
    run_platform_info(interpreter)
    run_script_execution(interpreter)
    run_dynamic_code_generation(interpreter)
    run_visualization_example(interpreter)


def run_docker_interpreter_examples():
    """Run all examples using the Docker Interpreter"""
    print("\n===== DOCKER INTERPRETER EXAMPLES =====\n")
    print("Running Docker interpreter examples...")
    
    try:
        # Initialize the Docker interpreter with a standard Python image
        interpreter = DockerInterpreter(
            image_tag="python:3.9-slim",  # Using official Python image
            print_stdout=True,
            print_stderr=True,
            container_directory="/app"  # Better working directory for containerized apps
        )
        
        # Run the examples
        run_simple_hello_world(interpreter)
        run_math_example(interpreter)
        run_platform_info(interpreter)
        run_script_execution(interpreter)
        run_dynamic_code_generation(interpreter)
        run_visualization_example(interpreter)
    except Exception as e:
        print(f"Error running Docker interpreter examples: {str(e)}")
        print("Make sure Docker is installed and running on your system.")
        print("You may need to pull the python:3.9-slim image first using: docker pull python:3.9-slim")


def run_mcp_example():
    """
    Run an example using the MCP toolkit to search for job information about 'data scientist'.
    This uses the sample_mcp.config file to configure the MCP client.
    """
    print("\n===== MCP TOOLKIT EXAMPLE =====\n")
    
    # Get the path to the sample_mcp.config file
    config_path = os.path.join(os.getcwd(), "examples", "sample_mcp.config")
    
    print(f"Loading MCP configuration from: {config_path}")
    
    try:
        # Initialize the MCP toolkit with the sample config
        toolkit = MCPToolkit(config_path=config_path)
        
        # Get all available tools
        tools = toolkit.get_tools()
        
        print(f"Available MCP tools: {len(tools)}")
        for i, tool in enumerate(tools):
            print(f"Tool {i+1}: {tool.name}")
            print(f"Description: {tool.descriptions[0]}")
            print("-" * 30)
        
        # Find and use the hirebase search tool
        hirebase_tool = None
        for tool in tools:
            if "hire" in tool.name.lower() or "search" in tool.name.lower():
                hirebase_tool = tool
                break
        
        if hirebase_tool:
            print(f"Using tool: {hirebase_tool.name}")
            
            # Search for 'data scientist' job information
            search_query = "data scientist"
            print(f"Searching for job information about: '{search_query}'")
            
            # Call the tool with the search query
            # Note: The actual parameter name might differ based on the tool's schema
            result = hirebase_tool.tools[0](**{"query": search_query})
            
            print("\nSearch Results:")
            print("-" * 50)
            print(result)
            print("-" * 50)
        else:
            print("No suitable hiring or search tool found in the MCP configuration.")
    except Exception as e:
        print(f"Error running MCP example: {str(e)}")
        print("Make sure the hirebase MCP server is properly configured with a valid API key.")
    finally:
        if 'toolkit' in locals():
            toolkit.disconnect()


def run_file_tool_example():
    """
    Run an example using the FileTool to read and write PDF files.
    """
    print("\n===== FILE TOOL EXAMPLE =====\n")
    
    try:
        # Initialize the file tool
        file_tool = FileTool()
        
        # Create sample content for a PDF
        sample_content = """This is a sample PDF document created using the FileTool.
This tool provides special handling for different file types.
For PDF files, it uses PyPDF2 library for reading and writing operations."""
        
        # Example PDF file path
        pdf_path = os.path.join(os.getcwd(), "examples", "output", "sample_document.pdf")
        
        # Make sure the output directory exists
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        
        print(f"Writing content to PDF file: {pdf_path}")
        
        # Write content to PDF file
        write_result = file_tool.write_file(pdf_path, sample_content)
        print("Write Result:")
        print("-" * 30)
        print(write_result)
        print("-" * 30)
        
        # Read content from PDF file
        print(f"\nReading content from PDF file: {pdf_path}")
        read_result = file_tool.read_file(pdf_path)
        print("Read Result:")
        print("-" * 30)
        print(read_result)
        print("-" * 30)
        
        # Also demonstrate with a regular text file
        text_path = os.path.join(os.getcwd(), "examples", "output", "sample_text.txt")
        
        print(f"\nWriting content to text file: {text_path}")
        text_write_result = file_tool.write_file(text_path, "This is a sample text file.")
        print("Text Write Result:")
        print("-" * 30)
        print(text_write_result)
        print("-" * 30)
        
        print(f"\nReading content from text file: {text_path}")
        text_read_result = file_tool.read_file(text_path)
        print("Text Read Result:")
        print("-" * 30)
        print(text_read_result)
        print("-" * 30)
        
    except Exception as e:
        print(f"Error running file tool example: {str(e)}")


def run_browser_tool_example():
    """
    Run an example using the BrowserTool to initialize browser, 
    go to Google, search for "test", and then close the browser.
    """
    print("\n===== BROWSER TOOL EXAMPLE =====\n")
    
    try:
        # Initialize the browser tool (with visible browser window if headless is False)
        # browser_tool = BrowserTool(headless=False, timeout=10)
        browser_tool = BrowserTool(headless=True, timeout=10)
        
        print("Step 1: Initializing browser...")
        init_result = browser_tool.initialize_browser()
        print("Browser Initialization Result:")
        print("-" * 30)
        print(init_result)
        print("-" * 30)
        
        if init_result.get("status") == "success":
            print("\nStep 2: Navigating to Google...")
            nav_result = browser_tool.navigate_to_url("https://www.google.com")
            print("Navigation Result:")
            print("-" * 30)
            print(f"Status: {nav_result.get('status')}")
            print(f"URL: {nav_result.get('current_url')}")
            print(f"Title: {nav_result.get('title')}")
            
            # Show available interactive elements
            if nav_result.get("snapshot") and nav_result["snapshot"].get("interactive_elements"):
                elements = nav_result["snapshot"]["interactive_elements"]
                print(f"Found {len(elements)} interactive elements:")
                for elem in elements[:5]:  # Show first 5 elements
                    print(f"  - {elem['id']}: {elem.get('description', 'No description')}")
            print("-" * 30)
            
            if nav_result.get("status") == "success":
                # Find the search input box and search button
                elements = nav_result.get("snapshot", {}).get("interactive_elements", [])
                search_input_ref = None
                search_button_ref = None
                
                for elem in elements:
                    desc = elem.get("description", "").lower()
                    if "search" in desc and ("input" in desc or "textbox" in desc):
                        search_input_ref = elem["id"]
                    elif "search" in desc and ("button" in desc or "submit" in desc):
                        search_button_ref = elem["id"]
                
                if search_input_ref:
                    print(f"\nStep 3: Typing 'test' in search box (element {search_input_ref})...")
                    input_result = browser_tool.input_text(
                        element="Search box", 
                        ref=search_input_ref, 
                        text="test", 
                        submit=False
                    )
                    print("Input Result:")
                    print("-" * 30)
                    print(input_result)
                    print("-" * 30)
                    
                    if search_button_ref:
                        print(f"\nStep 4: Clicking search button (element {search_button_ref})...")
                        click_result = browser_tool.browser_click(
                            element="Search button", 
                            ref=search_button_ref
                        )
                        print("Click Result:")
                        print("-" * 30)
                        print(click_result)
                        print("-" * 30)
                    else:
                        print("\nStep 4: Search button not found, submitting with Enter key...")
                        submit_result = browser_tool.input_text(
                            element="Search box", 
                            ref=search_input_ref, 
                            text="", 
                            submit=True
                        )
                        print("Submit Result:")
                        print("-" * 30)
                        print(submit_result)
                        print("-" * 30)
        
        print("Closing browser...")
        close_result = browser_tool.close_browser()
        print("Browser Close Result:")
        print("-" * 30)
        print(close_result)
        print("-" * 30)
        
    except Exception as e:
        print(f"Error running browser tool example: {str(e)}")
        # Make sure to close browser even if there's an error
        try:
            if 'browser_tool' in locals():
                browser_tool.close_browser()
        except:
            pass


def main():
    """Main function to run all examples"""
    print("===== INTERPRETER TOOL EXAMPLES =====")
    
    # Run file tool example
    run_file_tool_example()
    
    # Run browser tool example
    run_browser_tool_example()
    
    
    # Run MCP toolkit example
    run_mcp_example()
    
    # # Run Python interpreter examples
    run_python_interpreter_examples()
    
    # # Run Docker interpreter examples
    run_docker_interpreter_examples()
    
    # # Run search tools examples
    run_search_examples()
    
    print("\n===== ALL EXAMPLES COMPLETED =====")


if __name__ == "__main__":
    main() 