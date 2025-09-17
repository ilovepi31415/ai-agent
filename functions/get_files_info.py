import os

def get_files_info(working_directory, directory="."):
    try:
        joined_dir = os.path.join(working_directory, directory)
        if not os.path.abspath(joined_dir).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        print(joined_dir)
        if not os.path.isdir(joined_dir):
            return f'Error: "{directory}" is not a directory'
        file_string = ''
        for path in os.listdir(joined_dir):
            true_path = os.path.join(joined_dir, path)
            file_string += f"- {path}: file_size={os.path.getsize(true_path)}, is_dir={os.path.isdir(true_path)}\n"
        return file_string
    except Exception as e:
        return f"Error: {e}"