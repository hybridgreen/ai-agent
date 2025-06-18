import os , sys
from google import genai
from google.genai import types # type: ignore 
from dotenv import load_dotenv # type: ignore

def main():

    3
    model = "gemini-2.0-flash-001"
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
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
    
if __name__ == "__main__":
    main