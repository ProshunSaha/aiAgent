import os
from google.genai import types


def get_files_info(working_directory, directory = "."):
    abs_working_dir = os.path.abspath(working_directory)
    abs_directory=""
    if directory is None:
        abs_directory = os.path.abspath(working_directory)
    else:
        abs_directory = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_directory.startswith(abs_working_dir):
        return f'Error: {directory} is not a directory'
    

    final_response = ""
    contents = os.listdir(abs_directory)

    for content in contents:
        content_path = os.path.join(abs_directory, content)
        is_dir = os.path.isdir(content_path)
        size = os.path.getsize(content_path)

        final_response += f"- {content}: file_size={size} bytes, is_dir={is_dir}\n"
    return final_response


# The new dictionary-based schema
schema_get_files_info = {
    "name": "get_files_info",
    "description": "Lists files and directories in a given path. Use '.' to list the root directory.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "working_directory": {
                "type": "STRING",
                "description": "The root directory (e.g., 'calculator')."
            },
            "directory": {
                "type": "STRING",
                "description": "The sub-directory to list, relative to the working directory. Use '.' for the root."
            }
        },
        "required": ["working_directory", "directory"]
    }
}