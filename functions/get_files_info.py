import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    path = os.path.abspath(working_directory)
    path_joined = os.path.join(path, directory)
    normalised_path = os.path.normpath(path_joined)
    dir_check = os.path.commonpath([path, normalised_path]) == path
    if dir_check is False:
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
    elif os.path.isdir(normalised_path) is False:
        return f"Error: \"{directory}\" is not a directory"
    elif dir_check is True:
        list_of_messages = []
        try:
            for i in os.listdir(normalised_path):
                name = i
                file_size = os.path.getsize(os.path.join(normalised_path, i))
                is_dir = os.path.isdir(os.path.join(normalised_path, i))
                list_of_messages.append(f"- {name}: file_size={file_size} bytes, is_dir={is_dir}")
            return f"Result for {directory}:\n{"\n".join(list_of_messages)}"
        except Exception as e:
            return f"Error: {e}" 
    else:
        raise Exception("Error: another unknown error occurred")
