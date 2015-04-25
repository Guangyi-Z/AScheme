
class Symbol(str): pass

def Sym(s, symbol_table={}):
    "Find or create unique Symbol entry for str s in symbol table."
    if s not in symbol_table: symbol_table[s] = Symbol(s)
    return symbol_table[s]

_quote, _if, _set, _define, _lambda, _begin, _definemacro, = map(Sym,
"quote   if   set!  define   lambda   begin   define-macro".split())

_quasiquote, _unquote, _unquotesplicing = map(Sym,
"quasiquote   unquote   unquote-splicing".split())

_spawn, _join, _value = map(Sym,
"spawn join value".split())

_defineactor, _spawnactor, _startactor, _joinactor = map(Sym,
"define-actor spawn-actor start-actor join-actor".split())

_send, _rcv, _makemsg, _getinfo, _getsender = map(Sym,
"! rcv make-msg get-info get-sender".split())

eof_object = Symbol('#<eof-object>') # Note: uninterned; can't be read
