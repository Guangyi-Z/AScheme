from nose.tools import *
import unittest
from AScheme.tokenizer import InPort

class TestTokenizer(unittest.TestCase):

    def test_tokenizer(self):
        program = "(begin (define r 10) (* pi (* r r)))"
        inport = InPort(program)
        res = ['(', 'begin', '(', 'define', 'r', '10', ')', '(', '*', 'pi', '(', '*', 'r', 'r', ')', ')', ')']
        for token in res:
            self.assertEqual(token, inport.next_token())

