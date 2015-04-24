from nose.tools import *
import unittest
from AScheme.parse import parse
from AScheme.eval import eval
from AScheme.util import to_string

spawn_tests = [
    ('''
    (define f (lambda (beg end)
        (if (= beg end)
        end
        (+ beg
            (f (+ beg 1) end)))))''', None),
    ("(define f1 (spawn f 1 100))", None),
    ("(define f2 (spawn f 101 200))", None),
    ("(join f1 f2)", None),
    ("(value f1)", 5050),
    ("(value f2)", 15050),
    ("(+ (value f1) (value f2))", 20100),
    ("(value (spawn f 1 100))", 5050),
]

class TestEvaluator(unittest.TestCase):

    def f(self, tests):
        for (x, expected) in tests:
            result = None
            try:
                result = eval(parse(x))
            except Exception as e:
                try:
                    self.assertTrue(
                        issubclass(expected, Exception) and isinstance(e, expected),
                        x + ' =raises=> ' + type(e).__name__ + str(e))
                except Exception as e2:
                    print x, '=>', expected
                    raise e
            else:
                self.assertEqual(result,
                                 expected, x + ' => ' + to_string(result))

    def test_spawn(self):
        self.f(spawn_tests)

    # def test_actor(self):
    #     src = '''
    #     (defactor Ping (start)
    #       (receive (m)
    #         (print 'ping')
    #         (! (get-sender m) 'pong')))
    #     (defactor Pong (start)
    #       (receive (m)
    #         (print 'pong')
    #         (! (get-sender m) 'ping')))
    #     (define ping (spawn-actor Ping 5))
    #     (define pong (spawn-actor Pong 5))
    #     '''

    #     self.assertEqual(None, eval_all(parse_all(src)))
