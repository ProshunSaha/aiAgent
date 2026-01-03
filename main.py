import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import  schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import  schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function



def main():


    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)  


    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read the content of a file
- Write to a file (create of update)
- Run a python file with optional arguments

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


    if len(sys.argv) < 2:
        print("You need to provide a prompt!")
        sys.exit(1)

    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text = prompt)])
    ]

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
        ]
    )   
    
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt   
    )   

    for i in range(20):
        print(f"\n--- Iteration {i + 1} ---")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=messages,
            config=config
        )

        # Add model's response to history
        messages.append(response.candidates[0].content)

        function_responses = []
        found_tool_call = False
        
        # First, check if there are ANY function calls in this turn
        for part in response.candidates[0].content.parts:
            if part.function_call:
                found_tool_call = True
                break

        # Process parts
        for part in response.candidates[0].content.parts:
            if part.function_call:
                print(f"Action: Calling {part.function_call.name}...")
                tool_response_content = call_function(part.function_call, verbose_flag)
                function_responses.append(tool_response_content.parts[0])
            
            elif part.text:
                print(f"Agent Thought: {part.text}")

        # Final check for the loop
        if found_tool_call:
            # We have tool results to send back
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            # No tools were called, this is the final answer
            print("\n--- Task Complete ---")
            return

    print("\nError: Maximum iterations reached.")
    sys.exit(1)






if __name__ == "__main__":
    main()