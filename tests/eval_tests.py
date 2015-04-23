from nose.tools import *
import unittest
import sys
import StringIO
from AScheme.lispy import parse
from AScheme.eval import eval
from AScheme.util import to_string

lis_tests = [
    ("(quote (testing 1 (2.0) -3.14e159))", ['testing', 1, [2.0], -3.14e159]),
    ("(+ 2 2)", 4),
    ("(+ (* 2 100) (* 1 10))", 210),
    ("(if (> 6 5) (+ 1 1) (+ 2 2))", 2),
    ("(if (< 6 5) (+ 1 1) (+ 2 2))", 4),
    ("(define x 3)", None),
    ("x", 3),
    ("(+ x x)", 6),
    ("(begin (define x 1) (set! x (+ x 1)) (+ x 1))", 3),
    ("((lambda (x) (+ x x)) 5)", 10),
    ("(define twice (lambda (x) (* 2 x)))", None), ("(twice 5)", 10),
    ("(define compose (lambda (f g) (lambda (x) (f (g x)))))", None),
    ("((compose list twice) 5)", [10]),
    ("(define repeat (lambda (f) (compose f f)))", None),
    ("((repeat twice) 5)", 20), ("((repeat (repeat twice)) 5)", 80),
    ("(define fact (lambda (n) (if (<= n 1) 1 (* n (fact (- n 1))))))", None),
    ("(fact 3)", 6),
    ("(fact 50)", 30414093201713378043612608166064768844377641568960512000000000000),
    ("(define abs (lambda (n) ((if (> n 0) + -) 0 n)))", None),
    ("(list (abs -3) (abs 0) (abs 3))", [3, 0, 3]),
    ("""(define combine (lambda (f)
    (lambda (x y)
    (if (null? x) (quote ())
        (f (list (car x) (car y))
            ((combine f) (cdr x) (cdr y)))))))""", None),
    ("(define zip (combine cons))", None),
    ("(zip (list 1 2 3 4) (list 5 6 7 8))", [[1, 5], [2, 6], [3, 7], [4, 8]]),
    ("""(define riff-shuffle (lambda (deck) (begin
    (define take (lambda (n seq) (if (<= n 0) (quote ()) (cons (car seq) (take (- n 1) (cdr seq))))))
    (define drop (lambda (n seq) (if (<= n 0) seq (drop (- n 1) (cdr seq)))))
    (define mid (lambda (seq) (/ (length seq) 2)))
    ((combine append) (take (mid deck) deck) (drop (mid deck) deck)))))""", None),
    ("(riff-shuffle (list 1 2 3 4 5 6 7 8))", [1, 5, 2, 6, 3, 7, 4, 8]),
    ("((repeat riff-shuffle) (list 1 2 3 4 5 6 7 8))",  [1, 3, 5, 7, 2, 4, 6, 8]),
    ("(riff-shuffle (riff-shuffle (riff-shuffle (list 1 2 3 4 5 6 7 8))))", [1,2,3,4,5,6,7,8]),
    ]

set_tests = [
    ("(set! x)", SyntaxError),

    ("(define ((account bal) amt) (set! bal (+ bal amt)) bal)", None),
    ("(define a1 (account 100))", None),
    ("(a1 0)", 100), ("(a1 10)", 110), ("(a1 10)", 120),
    ]

quote_tests = [
    ("(quote 1 2)", SyntaxError),
    ]

lispy_tests = [
    ("()", SyntaxError),
    ("(define 3 4)", SyntaxError),
    ("(if 1 2 3 4)", SyntaxError),
    ("(lambda 3 3)", SyntaxError),
    ("(lambda (x))", SyntaxError),

    ("(define (twice x) (* 2 x))", None),
    ("(twice 2)", 4),
    ("(twice 2 2)", TypeError),

    ("(define lyst (lambda items items))", None),
    ("(lyst 1 2 3 (+ 2 2))", [1,2,3,4]),

    ("(if 1 2)", 2),
    ("(if (= 3 4) 2)", None),

    ("""(define (newton guess function derivative epsilon)
          (define guess2 (- guess (/ (function guess) (derivative guess))))
          (if (< (abs (- guess guess2)) epsilon)
            guess2
            (newton guess2 function derivative epsilon)))"""
     , None),
    ("""(define (square-root a)
          (newton 1 (lambda (x) (- (* x x) a)) (lambda (x) (* 2 x)) 1e-8))"""
     , None),
    ("(> (square-root 200.) 14.14213)", True),
    ("(< (square-root 200.) 14.14215)", True),
    ("(= (square-root 200.) (sqrt 200.))", True),

    ("""(define (sum-squares-range start end)
          (define (sumsq-acc start end acc)
            (if (> start end)
              acc
              (sumsq-acc (+ start 1) end (+ (* start start) acc))))
          (sumsq-acc start end 0))"""
     , None),
    ("(sum-squares-range 1 3000)", 9004500500), ## Tests tail recursion
    ]

complex_tests = [
    ("(* 1i 1i)", -1),
    ("(sqrt -1)", 1j),
    ]

callcc_tests = [
    ("(call/cc (lambda (throw) (+ 5 (* 10 (throw 1))))) ;; throw", 1),
    ("(call/cc (lambda (throw) (+ 5 (* 10 1)))) ;; do not throw", 15),
    ("""(call/cc (lambda (throw)
         (+ 5 (* 10 (call/cc (lambda (escape) (* 100 (escape 3)))))))) ; 1 level""", 35),
    ("""(call/cc (lambda (throw)
         (+ 5 (* 10 (call/cc (lambda (escape) (* 100 (throw 3)))))))) ; 2 levels""", 3),
    ("""(call/cc (lambda (throw)
         (+ 5 (* 10 (call/cc (lambda (escape) (* 100 1))))))) ; 0 levels""", 1005),
]

macro_tests = [
    ("""(if (= 1 2) (define-macro a 'a)
     (define-macro a 'b))""", SyntaxError),

    ("(let ((a 1) (b 2)) (+ a b))", 3),
    ("(let ((a 1) (b 2 3)) (+ a b))", SyntaxError),

    ("(and 1 2 3)", 3),
    ("(and (> 2 1) 2 3)", 3),
    ("(and)", True),
    ("(and (> 2 1) (> 2 3))", False),

    ("""(define-macro unless (lambda args
          `(if (not ,(car args))
             (begin ,@(cdr args))))) ; test `"""
     , None),
    ("(unless (= 2 (+ 1 1)) (display 2) 3 4)", None),
    (r'(unless (= 4 (+ 1 1)) (display 2) (display "\n") 3 4)', 4),

    ("(quote x)", 'x'),
    ("(quote (1 2 three))", [1, 2, 'three']),

    ("'x", 'x'),
    ("'(one 2 3)", ['one', 2, 3]),

    ("(define L (list 1 2 3))", None),
    ("`(testing ,@L testing)", ['testing',1,2,3,'testing']),
    ("`(testing ,L testing)", ['testing',[1,2,3],'testing']),
    ("`,@L", SyntaxError),

    ("""'(1 ;test comments '
     ;skip this line
     2 ; more ; comments ; ) )
     3) ; final comment""", [1,2,3]),
    ]

literal_tests = [
    ("1", 1),
    ("2.5", 2.5),
    ("#t", True),
    ("#f", False),
    ("'hello'", "hello"),
    ('"hello"', "hello"),
    ]

io_tests = [
    ("(define o (open-output-file \"out1.txt\"))", None),
    ("(port? o)", True),
    ("(write 123 o)", None),
    ("(close-output-port o)", None),
    ("(define in (open-input-file \"out1.txt\"))", None),
    ("(port? in)", True),
    ("(read in)", 123),
    ("(close-input-port in)", None),

    ("(define o (open-output-file \"out2.txt\"))", None),
    ("(port? o)", True),
    ("(write \"hello\" o)", None),
    ("(close-output-port o)", None),
    ("(define in (open-input-file \"out2.txt\"))", None),
    ("(port? in)", True),
    ("(read in)", "hello"),
    ("(close-input-port in)", None),
    ]

class TestEval(unittest.TestCase):

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

    def test_lis(self):
        self.f(lis_tests)

    def test_lispy(self):
        self.f(lispy_tests)

    def test_set(self):
        self.f(set_tests)

    def test_complext(self):
        self.f(complex_tests)

    def test_quote(self):
        self.f(quote_tests)

    def test_literal(self):
        self.f(literal_tests)

    def test_io(self):
        # result = eval(parse("(open-output-file \"out1.txt\")"))
        # sys.stderr.write(result.__repr__())
        self.f(io_tests)

    def test_display(self):
        # 'hello world\n' doesn't work
        src = "(display \"hello world\")"

        saved_stdout = sys.stdout
        try:
            out = StringIO.StringIO()
            sys.stdout = out
            res = eval(parse(src))
            self.assertEqual(None, res)
            output = out.getvalue().strip()
            self.assertEqual('hello world', output)
        finally:
            sys.stdout = saved_stdout
