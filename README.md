##ActorScm

A toy Scheme interpreter written in Python, with extra built-in concurrency support, a simple Actor-Model framework.
Thus I call it **AScheme**.

The interpreter is built on top of [lispy](http://norvig.com/lispy2.html),
and the concurrency mechanism is based on Python’s ``gevent`` package.

###Try the Ping/Pong Examples

First get the environment and dependencies prepared.

```sh
virtualenv venv
source vene/bi/activate
pip install nose
pip install gevent
```

Then run the Ping/Pong example.

```
source vene/bi/activate
python run_examples.py
```

###Scheme’s Features

* Data Type: number, string, boolean, complex, quote, comment
* Function and Definition: ``define``, ``lambda``
* Logic: ``if``
* Macro System: ``define-macro``, so far macro ``let``, ``and``, ``cond`` have been implemented
* I/O: port
* Tail Call Optimization
* Call-with-current-continuation: ``call/cc``

Besides, a large number of built-in functions are provided, thanks to Python’s powerful utilities.

On the whole, AScheme is pretty complete compared to the standard, 
and it’s enough for you to write most of the Scheme programs.

###Concurrent Support

####Naive Concurrency

```scheme
(define f (lambda (beg end)
  (if (= beg end)
    end
    (+ beg
      (f (+ beg 1) end)))))

(define f1 (spawn f 1 100))
(define f2 (spawn f 101 200))
(join f1 f2)
(value f1)  ; => 5050
(value f2)  ; => 15050
(+ (value f1) (value f2))  ; => 20100

(value (spawn f 1 100))  ; => 5050
```

####Actor Model

Sender/Receiver example

```scheme
(define-actor (receiver)
  (let ((m (rcv)))
    (let ((msg (get-info m)))
      (display msg)
      (display "\n"))))
(define-actor (sender r)
  (! r "hello, world"))
(define r (spawn-actor receiver))
(define s (spawn-actor sender r))
(start-actor r s)
(sleep 1)
(join-actor r s)
```

Ping/Pong example

```scheme
(define-actor (Ping pong)
  (define (f)
    (let ((m (rcv)))
      (let ((info (get-info m)))
        (display "Ping < ")
        (display info)
        (display "\n")
        (cond ((= "finish" info) (! pong "finish") (display "Ping finished"))
              (else (display "ping") (display "\n") (! pong "ping") (f))))))
  (f))
(define-actor (Pong)
  (define (f)
    (let ((m (rcv)))
      (let ((info (get-info m))
            (sdr (get-sender m)))
        (display "Pong < ")
        (display info)
        (display "\n")
        (cond ((= "ping" info) (display "pong") (display "\n") (! sdr "pong") (f))
            (else (display "Pong finished"))))))
  (f))
(define pong (spawn-actor Pong))
(define ping (spawn-actor Ping pong))
(start-actor pong ping)
(! ping "pong")
(sleep 1)
(! ping "finish")
```

###Modules Dependency

```
┌──────────┐
│  InPort  │
└──────────┘
      ▲     
      │     
┌──────────┐
│   read   │
└──────────┘
      ▲     
      │     
┌──────────┐
│   Env    │
└──────────┘
      ▲     
      │     
┌──────────┐
│   eval   │
└──────────┘
      ▲     
      │     
┌──────────┐
│  expand  │
└──────────┘
      ▲     
      │     
┌──────────┐
│  parse   │
└──────────┘
```
