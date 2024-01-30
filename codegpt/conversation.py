import argparse
from dataclasses import dataclass
from enum import Enum


class Model(Enum):
    GPT_4 = "gpt-4-0125-preview"


def argparse_model_type(model_str):
    if model_str.lower() == "gpt-4-0125-preview":
        return Model.GPT_4
    else:
        raise argparse.ArgumentTypeError(f"Model {model_str} is not supported.")


@dataclass
class Conversation:
    messages: list[dict]
    model: Model
