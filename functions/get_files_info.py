import os , sys

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