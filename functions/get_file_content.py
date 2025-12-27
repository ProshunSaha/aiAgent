import os
from config import MAX_CHARS
from google.genai import types



def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: {file_path} is not in working directory"
    if not os.path.isfile(abs_file_path):
        return f"Error: {file_path} is not a file"
    
    file_content_string = ""

    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) >=MAX_CHARS:
                file_content_string+=f"[...File {file_path} truncated at 10000 characters]"
        return file_content_string
    except Exception as e:
        return f"Exception reading file: {e}"
    


# The new dictionary-based schema
schema_get_file_content = {
    "name": "get_file_content",
    "description": "Reads the text content of a file. Use this to examine code or data before editing or running it.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "working_directory": {
                "type": "STRING",
                "description": "The root directory (e.g., 'calculator')."
            },
            "file_path": {
                "type": "STRING",
                "description": "The path to the file relative to the working directory (e.g., 'main.py')."
            }
        },
        "required": ["working_directory", "file_path"]
    }
}