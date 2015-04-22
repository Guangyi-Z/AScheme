import sys
from util import isa, to_string, is_pair, cons, readchar
from symbol import Symbol, eof_object
from parser import read

class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    def __init__(self, parms=(), args=(), outer=None):
        # Bind parm list to corresponding args, or single parm to list of args
        self.outer = outer
        if isa(parms, Symbol):
            self.update({parms:list(args)})
        else:
            if len(args) != len(parms):
                raise TypeError('expected %s, given %s, '
                                % (to_string(parms), to_string(args)))
            self.update(zip(parms,args))
    def find(self, var):
        "Find the innermost Env where var appears."
        if var in self: return self
        elif self.outer is None: raise LookupError(var)
        else: return self.outer.find(var)

def add_globals(self):
    "Add some Scheme standard procedures."
    import math, cmath, operator as op
    self.update(vars(math))
    self.update(vars(cmath))
    self.update({
     '+':op.add, '-':op.sub, '*':op.mul, '/':op.div, 'not':op.not_,
     '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq,
     'equal?':op.eq,
     'eq?':op.is_,
     'length':len,
     'cons':cons,
     'car':lambda x:x[0],
     'cdr':lambda x:x[1:],
     'append':op.add,
     'list':lambda *x:list(x),
     'list?': lambda x:isa(x,list),
     'null?':lambda x:x==[],
     'symbol?':lambda x: isa(x, Symbol),
     'boolean?':lambda x: isa(x, bool),
     'pair?':is_pair,
     'port?': lambda x:isa(x,file),
     'apply':lambda proc,l: proc(*l),
     # 'eval':lambda x: eval(expand(x)),
     # 'load':lambda fn: load(fn),
     # 'call/cc':callcc,
     'open-input-file':open,
     'close-input-port':lambda p: p.file.close(),
     'open-output-file':lambda f:open(f,'w'),
     'close-output-port':lambda p: p.close(),
     'eof-object?':lambda x:x is eof_object,
     'read-char':readchar,
     'read':read,
     'write':lambda x,port=sys.stdout:port.write(to_string(x)),
     'display':lambda x,port=sys.stdout:port.write(x if isa(x,str) else to_string(x))})
    return self

global_env = add_globals(Env())

