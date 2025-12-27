import os
from google.genai import types


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: {file_path} is not in working dir"
    
    parent_dir=os.path.dirname(abs_file_path)
    
    if not os.path.isfile(parent_dir):
        try:
            os.makedirs(parent_dir, exist_ok=True)
        except Exception as e:
            return f"Could not create parent dirs: {parent_dir} = {e}" 
    
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
        return f"Successfully wrote to {file_path} ({len(content)} characters written)"
    except Exception as e:
        return f"Failed to write to file: {file_path}, {e}"
    

schema_write_file = {
    "name": "write_file",
    "description": "Writes content to a file. Automatically creates any missing parent directories. Use this to create new files or update existing ones.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "working_directory": {
                "type": "STRING",
                "description": "The root directory for the operation (e.g., 'calculator')."
            },
            "file_path": {
                "type": "STRING",
                "description": "The path to the file relative to the working directory (e.g., 'pkg/utils.py')."
            },
            "content": {
                "type": "STRING",
                "description": "The full text content to be written into the file."
            }
        },
        "required": ["working_directory", "file_path", "content"]
    }
} 