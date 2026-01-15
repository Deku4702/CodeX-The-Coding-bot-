from functions.write_file import write_file as put_file_content
def main():
    
    write_content = put_file_content("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(write_content)
    write_file = put_file_content("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(write_file)
    write_file = put_file_content("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(write_file)

main()