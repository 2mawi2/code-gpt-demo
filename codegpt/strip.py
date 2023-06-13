import re


def strip_cmd(cmd):
    return re.sub('`[^`]*(`|$)', r'\1', cmd)
