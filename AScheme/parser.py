from type import Symbol, Sym, eof_object
from type import _quote, _quasiquote, _unquote, _unquotesplicing
from tokenizer import InPort

def parse(inport):
    "Parse a program: read and expand/error-check it."
    return read(InPort(inport))

# def readchar(inport):
#     "Read the next character from an input port."
#     if inport.line != '':
#         ch, inport.line = inport.line[0], inport.line[1:]
#         return ch
#     else:
#         return inport.file.read(1) or eof_object

quotes = {"'":_quote, "`":_quasiquote, ",":_unquote, ",@":_unquotesplicing}
def read(inport):
    "Read a Scheme expression from an input port."
    def read_ahead(token):
        if '(' == token:
            L = []
            while True:
                token = inport.next_token()
                if token == ')': return L
                else: L.append(read_ahead(token))
        elif ')' == token: raise SyntaxError('unexpected )')
        elif token in quotes: return [quotes[token], read(inport)]
        elif token is eof_object: raise SyntaxError('unexpected EOF in list')
        else: return atom(token)
    # body of read:
    token1 = inport.next_token()
    return eof_object if token1 is eof_object else read_ahead(token1)

def atom(token):
    'Numbers become numbers; #t and #f are booleans; "..." string; otherwise Symbol.'
    if token == '#t': return True
    elif token == '#f': return False
    elif token[0] == '"': return token[1:-1].decode('string_escape')
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            try: return complex(token.replace('i', 'j', 1))
            except ValueError:
                return Sym(token)

