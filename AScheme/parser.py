from tokenizer import InPort, read

def parse(inport):
    "Parse a program: read and expand/error-check it."
    return read(InPort(inport))

