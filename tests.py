from functions.functions import get_files_info, get_file_content

def test_calculator():
    result = get_file_content("calculator", "main.py")
    print (f'File length: {len(result)} \nFile content:{result}')

    result = get_file_content("calculator", "pkg/calculator.py")
    print (f'File length: {len(result)} \nFile content:{result}')

    result = get_file_content("calculator", "/bin/cat")
    print (f'File length: {len(result)} \nFile content:{result}')    
    pass



if __name__ == "__main__":
    test_calculator()