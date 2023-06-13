import os
import platform
import re
import subprocess
import sys

import openai
from simple_term_menu import TerminalMenu

from conversation import Conversation
from parse_args import parse_code_gpt_args
from messages_builder import Context, build_conversation
from open_ai_adapter import stream_cmd_into_terminal
from parse_os import parse_operating_system


def main():
    args = parse_code_gpt_args()
    if args.verbose:
        print("Verbose mode enabled")

    operating_system = parse_operating_system(platform.system())
    shell = os.environ.get("SHELL")
    current_dir = os.getcwd()
    context = Context(
        shell=shell,
        operating_system=operating_system,
        directory=current_dir,
        model=args.model,
    )
    conversation = build_conversation(context)

    if args.verbose:
        print("Sent this conversation to OpenAI:")
        print(conversation)

    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if openai.api_key is None:
        print("To use codegpt please set the OPENAI_API_KEY environment variable")
        print("You can get an API key from https://beta.openai.com/account/api-keys")
        print("To set the environment variable, run:")
        print("export OPENAI_API_KEY=<your key>")
        sys.exit(1)

    response = fetch_and_print_cmd(conversation)

    process_action(args, conversation, response)


def extract_action_param(input, action):
    pattern = fr'.*{action}\((.+)\).*'
    match = re.search(pattern, input)

    if match and match.group(1).startswith("'") and match.group(1).endswith("'"):
        return match.group(1)[1:-1]

    if match:
        return match.group(1)
    else:
        return None


def process_action(args, conversation, response):
    if 'ask_for_refinement' in response:
        refine_software(conversation, response, args)
    elif 'execute_command' in response:
        cmd = extract_action_param(response, 'execute_command')
        show_command_options(conversation, cmd, args)
    elif 'end_programming_session' in response:
        print("Goodbye!")
    else:
        no_action_found(conversation, response, args)


def no_action_found(conversation, response, args):
    conversation.messages.append({"role": "user", "content": "not_a_valid_action"})
    response = fetch_and_print_cmd(conversation)
    process_action(args, conversation, response)


def self_reflect(args, conversation, thought):
    conversation.messages.append({"role": "assistant", "content": thought})
    response = fetch_and_print_cmd(conversation)
    process_action(args, conversation, response)


def fetch_and_print_cmd(conversation):
    cmds = stream_cmd_into_terminal(conversation)
    return cmds


def show_command_options(conversation: Conversation, cmd, args):
    options = ["execute"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 0:
        execute(conversation, cmd, args)


def read_input():
    return input("> ")


def refine_software(conversation: Conversation, response, args):
    refinement = read_input()
    conversation.messages.append({"role": "assistant", "content": response})
    conversation.messages.append({"role": "user", "content": refinement})
    response = fetch_and_print_cmd(conversation)
    process_action(args, conversation, response)


def execute(conversation: Conversation, cmd, args):
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        out = result.stdout
        error = result.stderr
        print(f"Stdout: {out}")
        print(f"Stderr: {error}")
        respond_with_terminal_output(conversation, cmd, out, error, args)
    except Exception as e:
        print(e)


def respond_with_terminal_output(conversation: Conversation, cmd, out, error, args):
    error = error[:300]
    out = out[:1000]
    conversation.messages.append({"role": "assistant", "content": f"execute_command({cmd})"})
    cmd_response = f"""Stdout: `{out}`\n---\nStderr: `{error}`"""
    conversation.messages.append({"role": "user", "content": cmd_response})
    cmd = fetch_and_print_cmd(conversation)
    process_action(args, conversation, cmd)


if __name__ == "__main__":
    main()
