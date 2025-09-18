import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    joined_path = os.path.join(working_directory, file_path)
    if not os.path.abspath(joined_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(joined_path):
        return f'Error: File "{file_path}" not found'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    process_args = ["python3", joined_path] + args
    try:
        process = subprocess.run(process_args, timeout=30, capture_output=True)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    stdout = process.stdout.decode().strip()
    stderr = process.stderr.decode().strip()
    if stderr == '' and stdout == '':
        return "No output produced"
    message = f"STDOUT: {stdout}\nSTDERR: {stderr}"
    if process.returncode != 0:
        message += f"\nProcess exited with code {process.returncode}"
    return message

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file and returns the output, contrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to be run, relative to the working directory"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                default=[],
                description="Optional. A list of the arguments, if any are needed, for running the python file"
            )
        }
    )
)