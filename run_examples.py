
from AScheme.repl import load

load("examples/sender_receiver.scm")
load("examples/ping_pong.scm")

# import StringIO
# from AScheme.parse import parse
# from AScheme.parser import read
# from AScheme.token import InPort
#
# res = read(InPort(StringIO.StringIO("""(cond ((= 1 2) 1)
#                      ((= 1 1) 2))""")))
# print res
# res = parse("""(cond ((= 1 2) 1)
#                      ((= 1 1) 2))""")
# print res
#
#
# res = read(InPort(StringIO.StringIO("""(cond (#t 1)
#                      (#f 2))""")))
# print res
# res = parse("""(cond (#t 1)
#                     (#f 2))""")
# print res


