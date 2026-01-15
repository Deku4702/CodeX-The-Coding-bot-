from functions.run_python_file import run_python_file

def test_run_python_file():
    
    file_test = run_python_file("calculator", "main.py")
    print(file_test)
    file_test = run_python_file("calculator", "tests.py")
    print(file_test)
    file_test = run_python_file("calculator", "../main.py")
    print(file_test)
    file_test = run_python_file("calculator", "nonexistent.py")
    print(file_test)
    file_test = run_python_file("calculator", "lorem.txt")
    print(file_test)
    
test_run_python_file()