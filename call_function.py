from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# --------------------------------------------------
# Function dispatcher (LLM → real Python functions)
# --------------------------------------------------

def call_function(function_call, verbose=False):
    """
    Executes the function requested by the LLM and returns
    a dict with the result.
    """

    # Safe extraction of function name
    function_name = function_call.get("name", "")
    arguments = function_call.get("arguments", {})

    if verbose:
        print(f"Calling function: {function_name}({arguments})")
    else:
        print(f" - Calling function: {function_name}")

    # Map function names to real callables
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    # Unknown function safeguard
    if function_name not in function_map:
        return {
            "result": f"Error: Unknown function: {function_name}"
        }

    # Copy args safely
    args = dict(arguments) if arguments else {}

    # Inject working directory (LLM never controls this)
    args["working_directory"] = "./calculator"

    # Call the function
    try:
        function_result = function_map[function_name](**args)
        return {
            "result": function_result
        }
    except Exception as e:
        return {
            "result": f"Error calling {function_name}: {str(e)}"
        }
