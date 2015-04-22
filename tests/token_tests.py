from nose.tools import *
import unittest
import StringIO
from AScheme.token import InPort

class TestToken(unittest.TestCase):

    def test_tokenizer(self):
        program = "(begin (define r 10) (* pi (* r r)))"
        inport = InPort(StringIO.StringIO(program))
        res = ['(', 'begin', '(', 'define', 'r', '10', ')', '(', '*', 'pi', '(', '*', 'r', 'r', ')', ')', ')']
        for token in res:
            self.assertEqual(token, inport.next_token())

