from ..utils import *

import ast

class T1(ast.NodeTransformer):
    def visit_Sub(_,n): return ast.copy_location(ast.Mult(),n)

def 𝓔(s,T,D):
    s = s.translate(s.maketrans(D))
    return eval(compile(T().visit(ast.parse(s,'','eval')),'','eval'))

print('Part 1:',sum(𝓔(l, T1, {'*':'-'}) for l in open(input_file())))

class T2(ast.NodeTransformer):
    def visit_Add(_,n): return ast.copy_location(ast.Mult(),n)
    def visit_Mult(_,n): return ast.copy_location(ast.Add(),n)

print('Part 2:',sum(𝓔(l, T2, {'+':'*','*':'+'}) for l in open(input_file())))
