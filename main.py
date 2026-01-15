import os
import argparse
import json
from openai import OpenAI
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import call_function

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file


def main():
    # =========================
    # STEP 1: Load API key
    # =========================
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )

    # =========================
    # STEP 2: CLI arguments
    # =========================
    parser = argparse.ArgumentParser()
    parser.add_argument("user_prompt", type=str)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    # =========================
    # STEP 3: Messages (OpenAI format)
    # =========================
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    # =========================
    # STEP 4: Tools (schemas only)
    # =========================
    tools = [
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]

    # =========================
    # STEP 5: Agent Loop (up to 20 iterations)
    # =========================
    max_iterations = 20
    for iteration in range(max_iterations):
        if args.verbose:
            print(f"\n--- Iteration {iteration + 1} ---")

        # Call the model
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0,
        )

        message = response.choices[0].message

        # Add the assistant's response to messages
        assistant_message = {
            "role": "assistant",
            "content": message.content or "",
        }
        
        if message.tool_calls:
            assistant_message["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    }
                }
                for tc in message.tool_calls
            ]
        
        messages.append(assistant_message)

        # =========================
        # STEP 6: Handle tool calls
        # =========================
        if message.tool_calls:
            tool_results = []

            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                if args.verbose:
                    print(f"Calling function: {function_name}({arguments})")
                else:
                    print(f" - Calling function: {function_name}")

                function_result = call_function(
                    {
                        "name": function_name,
                        "arguments": arguments,
                    },
                    verbose=args.verbose,
                )

                # Print the tool result directly (for run_python_file output)
                result_content = function_result["result"]
                if result_content and not args.verbose:
                    print(result_content)

                tool_results.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": result_content,
                })

            # Add all tool results to messages
            for tool_result in tool_results:
                messages.append(tool_result)

        else:
            # No tool calls - model has finished
            print("Final response:")
            print(message.content)
            break

    else:
        # Loop ended without a final response
        print("ERROR: Maximum iterations reached without a final response from the model.")
        exit(1)


if __name__ == "__main__":
    main()

