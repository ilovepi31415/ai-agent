import os
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

available_functions = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(call, verbose):
    if verbose:
        print(f"Calling function: {call.name}({call.args})")
    else:
        print(f"Calling function: {call.name}")
    # If the function isn't available, return an error
    if call.name not in available_functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=call.name,
                    response={"error": f"Unknown function: {call.name}"},
                )
            ],
        )
    # Actually call the function
    response = available_functions[call.name]("./calculator", **call.args)
    # Return the response
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=call.name,
            response={"result": response},
            )
        ],
    )

    