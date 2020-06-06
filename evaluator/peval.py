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


def eval_integer_infix_expression(_op, left, right) -> Object:
    if _op == TokenTypes.PLUS:
        return Integer(left.value + right.value)
    elif _op == TokenTypes.MINUS:
        return Integer(left.value - right.value)
    elif _op == TokenTypes.ASTERISK:
        return Integer(left.value * right.value)
    elif _op == TokenTypes.SLASH:
        return Integer(left.value // right.value)
    elif _op == TokenTypes.LT:
        mapper_key = "TRUE" if left.value < right.value else "FALSE"
        return singleton_mapper[mapper_key]
    elif _op == TokenTypes.GT:
        mapper_key = "TRUE" if left.value > right.value else "FALSE"
        return singleton_mapper[mapper_key]
    elif _op == TokenTypes.EQ:
        mapper_key = "TRUE" if left.value == right.value else "FALSE"
        return singleton_mapper[mapper_key]
    elif _op == TokenTypes.NOT_EQ:
        mapper_key = "TRUE" if left.value != right.value else "FALSE"
        return singleton_mapper[mapper_key]
    else:
        return singleton_mapper['NULL']


def eval_infix_expression(_op, left, right) -> Object:
    if isinstance(left, Integer) and isinstance(right, Integer):
        return eval_integer_infix_expression(_op, left, right)
    elif isinstance(left, Boolean) and isinstance(right, Boolean):
        if _op == TokenTypes.EQ:
            return left is right
        elif _op == TokenTypes.NOT_EQ:
            return left is not right

    return singleton_mapper['NULL']


def is_truthy(condition: Object):
    if condition is singleton_mapper['NULL']:
        return False
    elif condition is singleton_mapper['FALSE']:
        return False
    elif condition is singleton_mapper['TRUE']:
        return True
    else:
        return True


def eval_if_expression(node: ast.IfExpression):
    condition = eval(node._condition)

    if is_truthy(condition):
        return eval(node._consequence)
    elif node._alternative:
        return eval(node._alternative)
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

    if isinstance(node, ast.InfixExpression):
        left = eval(node._left)
        right = eval(node._right)
        return eval_infix_expression(node._op, left, right)

    if isinstance(node, ast.BlockStatement):
        return eval_statements(node._statements)

    if isinstance(node, ast.IfExpression):
        return eval_if_expression(node)

    return singleton_mapper['NULL']
