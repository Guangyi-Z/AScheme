
import StringIO
from token import InPort
from parser import read
from expand import expand

def parse(inport):
    "Parse a program: read and expand/error-check it."
    # Backwards compatibility: given a str, convert it to an InPort
    if isinstance(inport, str): inport = InPort(StringIO.StringIO(inport))
    return expand(read(inport), toplevel=True)

