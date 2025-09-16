import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=key)

if len(sys.argv) < 2:
    print("ERROR: no prompt provided")
    sys.exit(1)
prompt = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)])
]

response = client.models.generate_content(model='gemini-2.0-flash-001', contents=prompt)
print(response.text)
if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    print("User prompt:", prompt)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)