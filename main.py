import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import  schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import  schema_run_python_file
from functions.write_file import schema_write_file




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

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=messages,
        config = config)
    





    

    # 1. Check if the model wants to call a function
    # The SDK usually puts these in the first candidate's parts
    if response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.function_call:
                # 2. Print the call (added the print function)
                print(f"Model wants to call: {part.function_call.name}")
                print(f"Arguments: {part.function_call.args}")
                
                # Here is where you will eventually execute the local function
            elif part.text:
                print(part.text)
    else:
        print("No response parts found.")










    # print(response.text)
    if response is None or response.usage_metadata is None:
        print("Response is malformed")
        return

    if(verbose_flag == True):
        print(f"User Prompt is {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")



main()