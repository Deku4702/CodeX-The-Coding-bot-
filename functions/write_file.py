import os


def write_file(working_directory, file_path, content):
    
    try:
        working_directory = os.path.abspath(working_directory)
        target_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        
        if os.path.commonpath([working_directory, target_file_path]) != working_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.exists(target_file_path) and os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        parent_dir = os.path.dirname(target_file_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with open(target_file_path, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f'Error: Failed to write to "{file_path}": {str(e)}'

    
schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Creates or overwrites a file with the provided content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Text content to write into the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}
