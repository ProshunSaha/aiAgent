from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from google.genai import types

working_directory = "calculator"


def call_function(function_call_part, verbose=False):
    args = dict(function_call_part.args)
    
    if verbose:
        print(
            print(f"Calling function: {function_call_part.name} with args: {args}")
        )
    else:
        print(f"Calling function: {function_call_part.name}")

    
    # Overwrite whatever the model sent with our secure working_directory
    # This prevents the "multiple values" error
    args['working_directory'] = working_directory
    
    
    
    result = None

    if function_call_part.name == "get_files_info":
        result = get_files_info(
            
            **function_call_part.args
        )

    elif function_call_part.name == "get_file_content":
        result = get_file_content(
            
            **function_call_part.args
        )

    elif function_call_part.name == "run_python_file":
        result = run_python_file(
            
            **function_call_part.args
        )

    elif function_call_part.name == "write_file":
        result = write_file(
            
            **function_call_part.args
        )

    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={
                        "error": f"Unknown function: {function_call_part.name}"
                    }
                )
            ]
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result}
            )
        ]
    )
