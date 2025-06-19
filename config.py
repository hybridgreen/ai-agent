import os , sys
import os , sys
from google import genai
from google.genai import types # type: ignore 
from dotenv import load_dotenv # type: ignore

SYSTEM_PROMPT = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""

model_name = "gemini-2.0-flash-001"

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


