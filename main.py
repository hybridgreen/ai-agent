import os , sys
from google import genai
from google.genai import types
from dotenv import load_dotenv

def main():

    3
    model = "gemini-2.0-flash-001"
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    try:
        if len(sys.argv) < 2:
            raise Exception("Error, no prompt provided")
    except Exception:
        sys.exit(1)

    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
    ]

    response = client.models.generate_content(model=model,contents = messages)

    if len(sys.argv) >= 3:
        match sys.argv[2]:
            case "--verbose":
                print(f"User prompt: {sys.argv[1]}")
                print("Prompt tokens:",response.usage_metadata.prompt_token_count)
                print("Response tokens:",response.usage_metadata.candidates_token_count)
            
            

    
    print(response.text)
    
main()