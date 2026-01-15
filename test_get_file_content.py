from functions.get_file_content import get_file_content

def main():
    
    file_content = get_file_content("calculator", "lorem.txt")
    print(file_content)
    
    file_content = get_file_content("calculator", "main.py")
    print(file_content)
    
    file_content = get_file_content("calculator", "pkg/calculator.py")
    print(file_content)
    
    file_content = get_file_content("calculator", "/bin/cat")
    print(file_content)
    
    file_content = get_file_content("calculator", "pkg/does_not_exist.py")
    print(file_content)
    
main()