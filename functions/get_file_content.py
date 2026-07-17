import os
from config import MAX

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads content at the location provided by the user",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to read the content from",
                },
            },
            "required": ["file_path"]
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        wd_path = os.path.abspath(working_directory)
        joined_path = os.path.normpath(os.path.join(wd_path, file_path))
        if os.path.commonpath([wd_path, joined_path]) != wd_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif os.path.isfile(joined_path) is False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(joined_path, "r") as f:
                file_content_string = f.read(MAX)
                if f.read(1):
                    file_content_string += f"[...File \"{file_path}\"truncated at {MAX} characters]"
                return file_content_string
    except Exception as e:
        return f"Error: {e}"

