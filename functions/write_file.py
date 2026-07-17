import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes to a specified file at the file path using the content provided by the user",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to write the content to",
                },
                "content": {
                    "type": "string",
                    "description": "The content that will overwrite the file located at the file path or be in the newly generated file at the file path",
                },
            },
            "required": ["file_path", "content"]
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        wd_path = os.path.abspath(working_directory)
        joined_path = os.path.normpath(os.path.join(wd_path, file_path))
        if os.path.commonpath([wd_path, joined_path]) != wd_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(joined_path) is True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        else:
            os.makedirs(os.path.dirname(joined_path), exist_ok=True)
            with open(joined_path, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
