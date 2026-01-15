import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    """
    Executes a Python file in the given working directory with optional command-line arguments.
    Returns the exact stdout on success, or stdout+stderr with exit code on failure.
    """
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

        # Prevent directory traversal
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Ensure file exists and is a regular Python file
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build command safely
        command = ["python", abs_file_path]
        if args:
            command.extend(args)

        # Run the Python file
        result = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Combine stdout + stderr for full output
        full_output = (result.stdout or "") + (result.stderr or "")

        if result.returncode == 0:
            # On success, return the script's output exactly
            return full_output.strip()  # remove trailing newlines
        else:
            # On failure, include helpful info
            return f"Process exited with code {result.returncode}\n{full_output.strip()}"


    except Exception as e:
        return f"Error: executing Python file: {e}"


# Schema for AI tool
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file with optional command-line arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Python file path to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of command-line arguments",
                },
            },
            "required": ["file_path"],
        },
    },
}
