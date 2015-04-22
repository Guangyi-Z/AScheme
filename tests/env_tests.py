from nose.tools import *
import unittest
import StringIO
from AScheme.token import InPort
from AScheme.repl import repl

class TestEnv(unittest.TestCase):

    def test_parse(self):
        src = '''
        (define r 10)
        (* r r)
        '''
        inport = InPort(StringIO.StringIO(src))
        out = StringIO.StringIO()
        repl(inport=inport, out=out)
        output = out.getvalue().strip()
        self.assertEqual('100', output)

