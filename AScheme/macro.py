

# macro_table = {_let:let} ## More macros can go here
macro_table = {}

# def let(*args):
#     args = list(args)
#     x = [_let] + args
#     require(x, len(args)>1)
#     bindings, body = args[0], args[1:]
#     require(x, all(isa(b, list) and len(b)==2 and isa(b[0], Symbol)
#                    for b in bindings), "illegal binding list")
#     vars, vals = zip(*bindings)
#     return [[_lambda, list(vars)]+map(expand, body)] + map(expand, vals)


