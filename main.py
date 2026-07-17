import os
import sys
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
import prompts
from call_function import available_functions, call_function

def main():
    # parser setup to access args.user_prompt
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("invalid api key/api key not found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    model = "openrouter/free"
    
    messages = [
        {"role": "system", "content": prompts.system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    
    for i in range(20):
        response = client.chat.completions.create(model=model, messages=messages, tools=available_functions)
        
        message = response.choices[0].message
        
        if not response.usage.prompt_tokens:
            raise RuntimeError("no prompt tokens")
        else:
            messages.append(message)
            if args.verbose is True:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Response tokens: {response.usage.completion_tokens}")
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call=tool_call, verbose=args.verbose)
                if not result_message["content"]:
                    raise Exception(f"empty result from function: {tool_call.function.name}")
                else:
                    messages.append(result_message)
                    if args.verbose is True:
                        print(f"-> {result_message['content']}")
                        
        elif message.content:
            print(message.content)
            return
    print("The agent could not resolve the request")
    sys.exit(1)


if __name__ == "__main__":
    main()
