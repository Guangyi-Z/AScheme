from nose.tools import *
import unittest
import sys
import StringIO
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

sleep_tests = [
    ("(sleep 0.1)", None)
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

    def test_sleep(self):
        self.f(sleep_tests)

    def test_actor_echo(self):
        src = '''
        (begin
          (define-actor (echo s)
            (display s))
          (define e (spawn-actor echo \"hello, echo\"))
          (start-actor e)
          (sleep 0.1)
          (join-actor e))
        '''

        saved_stdout = sys.stdout
        try:
            out = StringIO.StringIO()
            sys.stdout = out
            eval(parse(src))
            output = out.getvalue().strip()
            self.assertEqual('hello, echo', output)
        finally:
            sys.stdout = saved_stdout

    def test_actor_send(self):
        src = '''
        (begin
          (define-actor (receiver)
            (let ((m (rcv)))
              (let ((msg (get-info m)))
                (display msg))))
          (define-actor (sender r)
            (! r "hello, world"))
          (define r (spawn-actor receiver))
          (define s (spawn-actor sender r))
          (start-actor r s)
          (sleep 0.1)
          (join-actor r s))
        '''

        saved_stdout = sys.stdout
        try:
            out = StringIO.StringIO()
            sys.stdout = out
            eval(parse(src))
            output = out.getvalue().strip()
            self.assertEqual('hello, world', output)
        finally:
            sys.stdout = saved_stdout

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
