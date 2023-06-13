from typing import List
import tiktoken


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":
        num_tokens = 0
        for message in messages:
            num_tokens += 4
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += -1
        num_tokens += 2
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.""")


def limit_message_history_to(max_tokens: int, messages: List[dict]) -> List[dict]:
    limited_messages = []
    total_tokens = 0
    for message in reversed(messages):
        message_tokens = num_tokens_from_messages([message])
        total_tokens += message_tokens
        if message["role"] == "system":
            limited_messages.append(message)
            continue
        if total_tokens <= max_tokens:
            limited_messages.append(message)
    return list(reversed(limited_messages))
