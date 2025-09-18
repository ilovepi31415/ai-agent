import os
import subprocess

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
