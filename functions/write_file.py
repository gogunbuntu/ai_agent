import os

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
