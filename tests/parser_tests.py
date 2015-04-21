from nose.tools import *
import unittest
from AScheme.parser import parse

class TestParser(unittest.TestCase):

    def test_parse(self):
        program = "(begin (define r 10) (* pi (* r r)))"
        res = ['begin', ['define', 'r', 10], ['*', 'pi', ['*', 'r', 'r']]]
        self.assertEqual(res, parse(program))

