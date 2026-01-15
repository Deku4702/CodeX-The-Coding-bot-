import os
from functions.config import MAX_CHARS


def get_file_content(working_directory, file_path):
    
    try:
        
        #working directory absolute path & target file path normalization
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        
        #security check to ensure target file is inside working directory
        if os.path.commonpath([working_dir_abs, target_file_path]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        #check if target is a file
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        #to read upto the MAX
        with open(target_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(MAX_CHARS)
            
            #Check if the file was truncated
            if f.read(1):
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            
        return content
        
    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads and returns the contents of a file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}
