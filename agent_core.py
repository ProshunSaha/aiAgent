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

class Agent:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        self.client = genai.Client(api_key=self.api_key)
        self.system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read the content of a file
- Write to a file (create of update)
- Run a python file with optional arguments

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
        self.available_functions = types.Tool(
            function_declarations=[
                schema_get_files_info,
                schema_get_file_content,
                schema_write_file,
                schema_run_python_file
            ]
        )
        self.config = types.GenerateContentConfig(
            tools=[self.available_functions],
            system_instruction=self.system_prompt
        )

    def run(self, prompt: str, verbose: bool = False):
        messages = [
            types.Content(role="user", parts=[types.Part(text=prompt)])
        ]

        output_log = []

        for i in range(20):
            print(f"\n--- Iteration {i + 1} ---")
            output_log.append(f"--- Iteration {i + 1} ---")

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=self.config
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
                    log_msg = f"Action: Calling {part.function_call.name}..."
                    print(log_msg)
                    output_log.append(log_msg)

                    tool_response_content = call_function(part.function_call, verbose)
                    function_responses.append(tool_response_content.parts[0])

                elif part.text:
                    log_msg = f"Agent Thought: {part.text}"
                    print(log_msg)
                    output_log.append(log_msg)

            # Final check for the loop
            if found_tool_call:
                # We have tool results to send back
                messages.append(types.Content(role="user", parts=function_responses))
            else:
                # No tools were called, this is the final answer
                final_msg = "\n--- Task Complete ---"
                print(final_msg)
                output_log.append(final_msg)

                # Extract the final answer text
                final_answer = ""
                for part in response.candidates[0].content.parts:
                    if part.text:
                        final_answer += part.text

                return {
                    "output": final_answer,
                    "logs": output_log
                }

        error_msg = "\nError: Maximum iterations reached."
        print(error_msg)
        output_log.append(error_msg)
        return {
            "output": "Error: Maximum iterations reached.",
            "logs": output_log
        }
