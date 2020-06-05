from typing import List

from abstract import Node
from lexer.monkey_lexer import TokenTypes
from .object import Object, Integer, Boolean, Null
from abstract import monkey_ast as ast

singleton_mapper = {
    'TRUE': Boolean(True),
    'FALSE': Boolean(False),
    'NULL': Null()
}


def eval_statements(statements: List[ast.Statement]) -> Object:
    for statement in statements:
        result = eval(statement)
    return result


def eval_bang_operator_expresssion(right):
    if right is singleton_mapper['TRUE']:
        return singleton_mapper['FALSE']
    elif right is singleton_mapper['FALSE']:
        return singleton_mapper['TRUE']
    elif right is singleton_mapper['NULL']:
        return singleton_mapper['TRUE']
    else:
        return singleton_mapper['FALSE']


def eval_hyphen_operator_expression(right):
    if not isinstance(right, Integer):
        return None
    return Integer(-right.value)


def eval_prefix_expression(_op, right) -> Object:
    if _op == TokenTypes.BANG:
        return eval_bang_operator_expresssion(right)
    elif _op == TokenTypes.MINUS:
        return eval_hyphen_operator_expression(right)
    else:
        return singleton_mapper['NULL']


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

    if isinstance(node, ast.BooleanLiteral):
        return singleton_mapper[node.token_literal().upper()]

    if isinstance(node, ast.Program):
        return eval_statements(node._statements)

    if isinstance(node, ast.ExpressionStatement):
        return eval(node._expression)

    if isinstance(node, ast.PrefixExpression):
        right = eval(node._right)
        return eval_prefix_expression(node._op, right)

    return singleton_mapper['NULL']
