import os
from google.genai import types

CHARACTER_LIMIT = 10000

def get_file_content(working_directory, file_path):
    try:
        joined_path = os.path.join(working_directory, file_path)
        print(joined_path)
        if not os.path.abspath(joined_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(joined_path):
            return f'Error: file not found or is not a regular file'
        f = open(joined_path)
        contents = f.read()
        if len(contents) > CHARACTER_LIMIT:
            return contents[:CHARACTER_LIMIT] + f'[...File "{file_path}" truncated at {CHARACTER_LIMIT} characters]'
        return contents
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the contents of a file, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to be outputted, relative to the working directory"
            )
        }
    )
)