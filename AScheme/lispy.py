################ Scheme Interpreter in Python

## (c) Peter Norvig, 2010; See http://norvig.com/lispy2.html

################ Symbol, Procedure, classes

from __future__ import division
import StringIO

from util import isa, to_string, require, is_pair, cons
from symbol import Symbol, Sym, eof_object
from symbol import _quote, _if, _set, _define, _lambda, _begin, _definemacro, _quasiquote, _unquote, _unquotesplicing
from token import InPort
from parser import read
from eval import eval
from expand import expand

################ parse, read, and user interaction

def parse(inport):
    "Parse a program: read and expand/error-check it."
    # Backwards compatibility: given a str, convert it to an InPort
    if isinstance(inport, str): inport = InPort(StringIO.StringIO(inport))
    return expand(read(inport), toplevel=True)

eval(parse("""(begin

(define-macro and (lambda args
   (if (null? args) #t
       (if (= (length args) 1) (car args)
           `(if ,(car args) (and ,@(cdr args)) #f)))))

;; More macros can also go here

)"""))

