import gevent
from gevent.queue import Queue
from gevent import Greenlet
from util import isa
from symbol import Symbol
from symbol import _quote, _if, _set, _define, _lambda, _begin
from symbol import _spawn, _join, _value
from symbol import _defineactor, _spawnactor, _startactor, _joinactor
from symbol import _send, _rcv, _makemsg, _getinfo, _getsender
from env import Env, global_env

class Procedure(object):
    "A user-defined Scheme procedure."
    def __init__(self, parms, exp, env):
        self.parms, self.exp, self.env = parms, exp, env
    def __call__(self, *args):
        return eval(self.exp, Env(self.parms, args, self.env))

class Actor(Greenlet):

    def __init__(self, func, *args):
        self.inbox = Queue()
        self.func = func
        self.args_ = list(args) # self.args is used by Greenlet internally
        Greenlet.__init__(self)

    def receive(self):
        message = self.inbox.get()
        return message

    def _run(self):
        self.running = True
        self.func(*self.args_)

class Message():
    def __init__(self, s):
        self.info = s
        self.sender = gevent.getcurrent()

    def get_info(self):
        return self.info

    def get_sender(self):
        return self.sender

################ eval (tail recursive)

def eval(x, env=global_env):
    """Evaluate an expression in an environment.
    Tail Recursion for if, begin and user-customized procedure.
    We are free to do that whenever the old value of x is no longer needed.
    """
    while True:
        if isa(x, Symbol):       # variable reference
            return env.find(x)[x]
        elif not isa(x, list):   # constant literal
            return x
        elif x[0] is _quote:     # (quote exp)
            (_, exp) = x
            return exp
        elif x[0] is _if:        # (if test conseq alt)
            (_, test, conseq, alt) = x
            x = (conseq if eval(test, env) else alt)
        elif x[0] is _set:       # (set! var exp)
            (_, var, exp) = x
            env.find(var)[var] = eval(exp, env)
            return None
        elif x[0] is _define:    # (define var exp)
            (_, var, exp) = x
            env[var] = eval(exp, env)
            return None
        elif x[0] is _lambda:    # (lambda (var*) exp)
            (_, vars, exp) = x
            return Procedure(vars, exp, env)
        elif x[0] is _begin:     # (begin exp+)
            for exp in x[1:-1]:
                eval(exp, env)
            x = x[-1]
        elif x[0] is _spawn:
            proc = eval(x[1], env)
            args = [eval(arg, env) for arg in x[2:]]
            g = gevent.spawn(proc, *args)
            return g
        elif x[0] is _join:
            for g in x[1:]:
                t = eval(g, env)
                t.join()
            return None
        elif x[0] is _value:
            if isa(x[1], list):
                g = eval(x[1], env)
                g.join()
            else:
                g = env.find(x[1])[x[1]]
                if not g.ready():
                    g.join()
            return g.value
        elif x[0] is _spawnactor:
            proc = eval(x[1], env)
            args = [eval(arg, env) for arg in x[2:]]
            g = Actor(proc, *args)
            return g
        elif x[0] is _startactor:
            for g in x[1:]:
                t = eval(g, env)
                t.start()
            return None
        elif x[0] is _joinactor:
            if isa(x[1], list):
                g = eval(x[1], env)
                g.join()
            return None
        elif x[0] is _send:
            rcv = eval(x[1], env)
            msg = eval(x[2], env)
            rcv.inbox.put(msg)
            return None
        elif x[0] is _rcv:
            return gevent.getcurrent().inbox.get()
        elif x[0] is _makemsg:
            return Message(eval(x[1], env))
        elif x[0] is _getinfo:
            msg = eval(x[1], env)
            return msg.get_info()
        elif x[0] is _getsender:
            msg = eval(x[1], env)
            return msg.get_sender()
        else:                    # (proc exp*)
            exps = [eval(exp, env) for exp in x]
            proc = exps.pop(0)
            if isa(proc, Procedure):
                x = proc.exp
                env = Env(proc.parms, exps, proc.env)
            else:
                return proc(*exps)

