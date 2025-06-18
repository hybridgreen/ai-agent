from functions.functions import get_files_info, get_file_content , write_file, run_python_file

def test_calculator():
    result = run_python_file('calculator','main.py' )
    print (f'Output:{result}')

    result = run_python_file("calculator", "tests.py")
    print (f'Output:{result}')

    result = run_python_file("calculator", "../main.py")
    print (f'Output:{result}')

    result = run_python_file("calculator", "nonexistent.py")
    print (f'Output:{result}')
if __name__ == "__main__":
    test_calculator()