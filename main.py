import os , sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.functions import *

def call_function(function_call_part, verbose=False):
    if verbose:
     print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
     print(f" - Calling function: {function_call_part.name}")

    working_dir = "./calculator"
    match function_call_part.name:
         case 'run_python_file':
             function_result = run_python_file(working_dir, **function_call_part.args)
             pass
         case 'write_file':
             function_result = write_file(working_dir, **function_call_part.args)
             pass
         case 'get_file_content':
            function_result = get_file_content(working_dir,**function_call_part.args)
            pass
         case 'get_files_info':
            function_result = get_files_info(working_dir,**function_call_part.args)
            pass
         case _:
             return types.Content(
                 role="tool",
                 parts=[
                     types.Part.from_function_response(
                         name=function_call_part.name,
                         response={"error": f"Unknown function: {function_call_part.name}"},
                         )
                    ],
                )
    return types.Content(role="tool",
                         parts=[
                             types.Part.from_function_response(
                                 name=function_call_part.name,
                                 response={"result": function_result},
                                 )
                            ],
                        )

def generate_content(args):

    SYSTEM_PROMPT = """
        You are a helpful AI coding agent.
        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files
        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

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
    
    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Prints out the content of files, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to read files from, relative to the working directory.",
                ),
            },
        ), 
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Runs a .py file and returns it's output and errors if any; constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path of the file to run, relative to the working directory.",
                ),
            },
        ), 
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Write a file to the provided path, if the provided path is a sub directory, creates it and returns an error. Constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path of the file to be writen, creating a new directory and subdirectory if provided with a directory path. Caution, it will overwrite any previous file"),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content of the file to be writen.",
                ),
            },
        ), 
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=SYSTEM_PROMPT
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=args[1])]),
    ]
    
    model_name = "gemini-2.0-flash-001"

    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=config,
)
    if response.function_calls:
        for call in response.function_calls:
            if "--verbose" in args:
                content = call_function(call, True)
            else:
                content = call_function(call)
    else:
        print(response.text)

    if not content.parts[0].function_response.response:
        raise Exception("Kaput")
    else:

        if "--verbose" in args:
            print(f"-> {content.parts[0].function_response.response['result']}")
    pass

def main():

    sys_args = sys.argv.copy()

    if len(sys_args) < 2:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    
    load_dotenv()
    
    generate_content(sys_args)
                
    
if __name__ == "__main__":
    main()