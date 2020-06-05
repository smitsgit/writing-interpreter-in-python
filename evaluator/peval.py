from typing import List

from abstract import Node
from .object import Object, Integer
from abstract import monkey_ast as ast


def eval_statements(statements: List[ast.Statement]) -> Object:
    for statement in statements:
        result = eval(statement)
    return result


def eval(node: Node) -> Object:
    """
    Remember that every node defined in AST module fulfills the Node interface.
    and thus can be passed to eval.
    This allows us to call eval recursively while evaluating on part of ast.

    Each AST node needs different form of evaluation and eval is the place where we
    decide which form of evaluation is needed

    As an example, lets say when we pass ast.Program node to eval(), what eval should do is
    then evaluate each of the ast.Program.statements by calling itself with single statement.
    The return value of the outer call is the return value of the last call
    :param node:
    :return:
    """
    if isinstance(node, ast.IntegerLiteral):
        return Integer(node._value)

    if isinstance(node, ast.Program):
        return eval_statements(node._statements)

    if isinstance(node, ast.ExpressionStatement):
        return eval(node._expression)
