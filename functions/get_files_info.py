import os


def get_files_info(working_directory, directory="."):
    try:
        # Absolute path of working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Build and normalize target directory path
        target_dir = os.path.normpath(
            os.path.join(working_dir_abs, directory)
        )

        # Security check: ensure target is inside working directory
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if target is a directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        result = ""
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            is_dir = os.path.isdir(item_path)
            file_size = os.path.getsize(item_path)
            result += f"- {item}: file_size={file_size} bytes, is_dir={is_dir}\n"

        return result.strip()

    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}