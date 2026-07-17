import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes the python script found at the provided parameter file_path with any args optionally provided by the user",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to execute python file from, relative to the working directory (default is the working_directory itself)",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "list of arguments provided by the user to be given to the executed python file at the file path",
                },
            },
            "required": ["file_path"]
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        wd_path = os.path.abspath(working_directory)
        joined_path = os.path.normpath(os.path.join(wd_path, file_path))
        if os.path.commonpath([wd_path,joined_path]) != wd_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif os.path.isfile(joined_path) is False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif joined_path.split(".")[-1] != "py":
            return f'Error: "{file_path}" is not a Python file'
        else:
            command = ["python3", joined_path]
            if args is not None:
                command.extend(args)
            comp_process = subprocess.run(command, capture_output=True, text=True, timeout=30)
            output_string = []
            if comp_process.returncode != 0:
                output_string.append(f"Process exited with code {comp_process.returncode}")
            if comp_process.stdout is None and comp_process.stderr is None:
                output_string.append("No output produced")
            else:
                output_string.append(f"STDOUT: {comp_process.stdout}")
                output_string.append(f"STDERR: {comp_process.stderr}")
            return " ".join(output_string)
    except Exception as e:
        return f"Error: executing Python file: {e}"
