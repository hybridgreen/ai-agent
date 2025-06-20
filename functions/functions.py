import os , subprocess

def get_files_info(working_directory, directory=None):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.join(abs_working_dir,directory)
    if not target_dir.startswith(abs_working_dir):
            print(f'Error: Cannot list "{target_dir}" as it is outside the permitted working directory')
    elif not os.path.isdir(target_dir):
            print(f'Error: "{target_dir}" is not a directory')
    else:
        try:
            files_info = list()
            for item in os.listdir(target_dir):
                item_path = os.path.join(target_dir,item)
                files_info.append(
                f'-{item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}'
                )
            return "\n".join(files_info)
        except Exception as e:
            print(f"Error: {e}")

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory,file_path))
    
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file_path):
         return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_file_path, 'r') as f:
            document = f.read(10000)
            if len(f.read()) > 10000:
                document += f'...File "{file_path}" truncated at 10000 characters'
            return document
    except Exception as e:
         return f'Error:{e}'

def write_file(working_directory, file_path, content):

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory,file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        try:
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    if os.path.exists(abs_file_path) and os.path.isdir(abs_file_path):
        return f'Error: "{file_path}" is a directory, not a file'
    
    try:
         with open(abs_file_path, 'w') as f:
              f.write(content)
    except Exception as e:
         return f'Error: {e}'
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory,file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
         return f'Error: File "{file_path}" not found.'
    
    if not abs_file_path[-3:0] == '.py':
        f'Error: "{file_path}" is not a Python file.'
    
    try:
        args = ['python3', abs_file_path]
        result = subprocess.run(args, capture_output= True, timeout=30, text= True)
        output = result.stdout
        if output == '':
             output = "No output produced."
        return_string = f'Ran {file_path} \nSTDOUT:{output} \nSTDERR:{result.stderr}\n ============================================== \n'
        if result.returncode != 0:
             return_string += f'Process exited with code{result.returncode}'
        return return_string

    except Exception as e:
         return f"Error: executing Python file: {e}"

