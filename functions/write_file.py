import os

def write_file(working_directory, file_path, content):
    try:
        joined_path = os.path.join(working_directory, file_path)
        if not os.path.abspath(joined_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        os.makedirs(os.path.dirname(joined_path), exist_ok=True)
        with open(joined_path, 'w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"