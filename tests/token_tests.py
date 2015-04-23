from nose.tools import *
import unittest
import StringIO
from AScheme.token import InPort

class TestToken(unittest.TestCase):

    def load_program(self, program, res):
        inport = InPort(StringIO.StringIO(program))
        for token in res:
            self.assertEqual(token, inport.next_token())

    def test_tokenizer(self):
        program = "(begin (define r 10) (* pi (* r r)))"
        res = ['(', 'begin', '(', 'define', 'r', '10', ')', '(', '*', 'pi', '(', '*', 'r', 'r', ')', ')', ')']
        self.load_program(program, res)

    def test_token_string(self):
        src = "(display \"hello world\")"
        res = ['(', 'display', '"hello world"', ')']
        self.load_program(src, res)

