import sys

import openai

from conversation import Conversation
from limiter import limit_message_history_to, num_tokens_from_messages
from strip import strip_cmd


def _create_chat_completion(conversation, n, stream=False):
    limited_messages = limit_message_history_to(1000, conversation.messages)
    return openai.ChatCompletion.create(
        model=conversation.model.value,
        messages=limited_messages,
        temperature=0,
        top_p=0.2,
        frequency_penalty=0,
        presence_penalty=0,
        n=n,
        stream=stream,
    )


def stream_cmd_into_terminal(conversation: Conversation, retries=0) -> str:
    if retries > 3:
        print("Error: OpenAI API is not responding. Please try again later.")
        sys.exit(1)
    try:
        response = _create_chat_completion(conversation, n=1, stream=True)
        print(f"\033[94m> ", end='')
        cmd = ""
        for chunk in response:
            if "content" in chunk["choices"][0]["delta"]:
                cmd_delta = chunk["choices"][0]["delta"]["content"]
                cmd_delta = strip_cmd(cmd_delta)
                print(cmd_delta, end='')
                sys.stdout.flush()
                cmd += cmd_delta
        print("\033[0m")
        return strip_cmd(cmd)
    except Exception as e:
        print(e)
        return stream_cmd_into_terminal(conversation, retries + 1)
