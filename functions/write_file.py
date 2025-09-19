import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        # Gets true path to file
        joined_path = os.path.join(working_directory, file_path)

        # Validation: makes sure file is within allowed directory       
        if not os.path.abspath(joined_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Makes any directories in file path that don't exist
        os.makedirs(os.path.dirname(joined_path), exist_ok=True)
        
        # Overwrites file content and returns success message
        with open(joined_path, 'w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file, overwriting any old data and creating any files or directories necessary, contstrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to be written to, relative to the working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the file"
            )
        }
    )
)