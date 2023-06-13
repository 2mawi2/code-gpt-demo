import argparse

from conversation import argparse_model_type, Model


def parse_code_gpt_args():
    parser = argparse.ArgumentParser(prog="codegpt", description="Code GPT")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="increase output verbosity"
    )
    parser.add_argument("-hist", action="store_true")
    parser.add_argument(
        "-m", "--model", type=argparse_model_type, default=Model.GPT_4,
        help="The model to use. Defaults to gpt-4."
    )
    args = parser.parse_args()
    return args
