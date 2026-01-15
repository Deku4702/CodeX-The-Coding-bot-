from openai import OpenAI
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function  # your executor

import os


# Load your OpenRouter API key
api_key = os.environ.get("OPENROUTER_API_KEY") or "YOUR_KEY"

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Define all schemas as tools
tools = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file
]

# User prompt
messages = [
    {"role": "system", "content": "You can use tools to read/write/run files."},
    {"role": "user", "content": "List files in the root directory"}
]

# Call OpenRouter / OpenAI model
response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# Get the first message from model
message = response.choices[0].message

# If model wants to call a function/tool
if message.tool_calls:
    for tool_call in message.tool_calls:
        # Execute the tool
        function_result = call_function(tool_call, verbose=True)

        # Send tool result back to model
        messages.append(message)  # previous model message
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_call.function.name,
            "content": function_result.parts[0].function_response.response
        })

    # Get final model response after tool execution
    final_response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages
    )

    print(final_response.choices[0].message.content)
else:
    print(message.content)
