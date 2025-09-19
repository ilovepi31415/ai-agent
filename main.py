import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
Your actions take place in a feedback loop of calling function and receiving return values from those functions. You are allowed up to 20 iterations.

⚠️ Do NOT provide a text response unless your task is fully completed.
Continue using function calls to gather information or perform actions.

Only return a final text response when:
- All necessary actions are complete
- You have all the required information
- You are ready to end the task

You are allowed up to 20 iterations.

To leave the feedback loop once all necessary actions are complete, use "I'M DONE" at the beginning of your resopnse.
"""

if len(sys.argv) < 2:
    print("ERROR: no prompt provided")
    sys.exit(1)
prompt = sys.argv[1]

verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)])
]
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_run_python_file,
        schema_get_file_content,
        schema_write_file,
    ]
)

iterations = 0
while iterations < 20:
    try:
        done = False
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions]
            )

        )

        for candidate in response.candidates:
            messages.append(types.Content(role="model", parts=candidate.content.parts))

        if response.function_calls != None:
            for call in response.function_calls:
                print(f"\033[93m- Calling function: {call.name}({call.args})\033[0m]")
                call_return = call_function(call, verbose)
                if verbose:
                    print(f"-> {call_return.parts[0].function_response.response}")
                messages.append(call_return)

        for candidate in response.candidates:
            if candidate.content.parts:
                for part in candidate.content.parts:
                    if isinstance(part, types.Part) and part.text and "I'M DONE" in part.text:
                        done = True
                        print("\033[92response:\033[0m", part.text)
                        break
        if done:
            if verbose:
                print("User prompt:", prompt)
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print("Response tokens:", response.usage_metadata.candidates_token_count)
            break
        iterations += 1
    except Exception as e:
        print(f"Error: {e}")
        break