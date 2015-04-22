from nose.tools import *
import unittest
import StringIO
from AScheme.token import InPort
from AScheme.parser import read

class TestParser(unittest.TestCase):

    def test_parse(self):
        program = "(begin (define r 10) (* pi (* r r)))"
        inport = InPort(StringIO.StringIO(program))
        res = ['begin', ['define', 'r', 10], ['*', 'pi', ['*', 'r', 'r']]]
        self.assertEqual(res, read(inport))

