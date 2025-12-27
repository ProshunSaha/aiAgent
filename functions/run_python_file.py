import os
import subprocess
from google.genai import types



def run_python_file(working_directory:str, file_path: str, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: {file_path} is not in working directory"
    if not os.path.isfile(abs_file_path):
        return f"Error: {file_path} is not a file"
    if not abs_file_path.endswith(".py"):
        return f"Error: {file_path} is not a Python file"
    
    try:
        final_args = ["python3", file_path]
        final_args.extend(args)
        output = subprocess.run(
            final_args,
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True,
            text=True
            
        )
        final_string = f"""
STDOUT: {output.stdout}
STDERR: {output.stderr}
"""
        
        if output.stdout =="" and output.stderr == "":
            final_string = "No output produced\n"
        if output.returncode!=0:
            final_string +=f"Process exited with code {output.returncode}"
        return final_string
        
    except Exception as e:
        return f"Error: executing Python file: {e}"
        

# Change your bottom section to this:
schema_run_python_file = {
    "name": "run_python_file",
    "description": "Runs a python file with a python3 interpreter. Use '.' for the current root directory.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "working_directory": {
                "type": "STRING", 
                "description": "The directory to run the script from"
            },
            "file_path": {
                "type": "STRING",
                "description": "The name of the .py file to execute"
            },
            "args": {
                "type": "ARRAY",
                "items": {"type": "STRING"},
                "description": "Optional list of command line arguments",
            },
        },
        "required": ["working_directory", "file_path"]
    },
}