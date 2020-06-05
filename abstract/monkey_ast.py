from interface import implements, Interface
from typing import List
from lexer.monkey_lexer import Token


class Node(Interface):
    def token_literal(self) -> str:
        pass


class Statement(implements(Node)):
    def token_literal(self) -> str:
        pass

    def statement_node(self):
        pass


class Expression(implements(Node)):
    def token_literal(self) -> str:
        pass

    def expression_node(self):
        pass

    def __str__(self):
        pass


class PrefixExpression(Expression):
    def __init__(self, token: Token, operator: str, right: Expression = None):
        self._token = token
        self._op = operator
        self._right = right

    def token_literal(self) -> str:
        pass

    def expression_node(self):
        pass

    def __str__(self):
        return f"({self._op}{self._right})"


class InfixExpression(Expression):
    def __init__(self, token: Token, operator: str, left: Expression = None, right: Expression = None):
        self._token = token
        self._op = operator
        self._left = left
        self._right = right

    def token_literal(self) -> str:
        pass

    def expression_node(self):
        pass

    def __str__(self):
        return f"({self._left} {self._op} {self._right})"


class Identifier(Expression):
    """
    In Monkey language, identifier in let statement doesn't produce a value
    so why is it implementing a Expression interface ?

    Identifiers in other parts of Monkey language do produce a value
    let x = valueProducingIdentifier

    And to keep the number of different nodes small, We will use identifier here to
    represent the name in a variable binding and later reuse it to represent an
    Identifier as part of the complete expression.
    """

    def __init__(self, token: Token, value: Expression):
        self._token = token  # TokenTypes.IDENT token
        self._value = value

    def token_literal(self) -> str:
        return self._token.literal

    def expression_node(self):
        pass

    def __str__(self):
        return f"{self._value}"


class BooleanLiteral(Expression):
    def __init__(self, token: Token, value: bool):
        self._token = token
        self._value = value

    def token_literal(self) -> str:
        return self._token.literal

    def expression_node(self):
        pass

    def __str__(self):
        return f"{self._token.literal}"


class IntegerLiteral(Expression):
    def __init__(self, token: Token, value: int):
        self._token = token
        self._value = value

    def token_literal(self) -> str:
        return self._token.literal

    def expression_node(self):
        pass

    def __str__(self):
        return f"{str(self._value)}"


class LetStatement(Statement):
    def __init__(self, token: Token, name: Identifier = None, value: Expression = None):
        self._token = token  # TokenTypes.LET token
        self._name = name
        self._value = value

    def token_literal(self) -> str:
        return self._token.literal

    def statement_node(self):
        pass

    def __str__(self):
        repr = f"{self.token_literal()} {self._name} = "
        if self._value:
            repr = repr + f"{str(self._value)};"

        return repr


class ReturnStatement(Statement):
    def __init__(self, token: Token, value: Expression = None):
        self._token = token  # TokenTypes.RETURN
        self._value = value

    def token_literal(self) -> str:
        return self._token.literal

    def statement_node(self):
        pass

    def __str__(self):
        repr = f"{self.token_literal()}"
        if self._value:
            repr = f"{repr} {self._value};"

        return repr


class ExpressionStatement(Statement):
    def __init__(self, token: Token, expression: Expression = None):
        self._token = token  # The first token of the expression
        self._expression = expression

    def token_literal(self) -> str:
        pass

    def statement_node(self):
        pass

    def __str__(self):
        if self._expression:
            repr = f"{self._expression}"
            return repr

        return ""


class BlockStatement:
    def __init__(self, token: Token, statements: List[Statement] = None):
        self._token = token  # The '{' token
        self._statements = statements

    def token_literal(self) -> str:
        return self._token.literal

    def statement_node(self):
        pass

    def __str__(self):
        data = ""
        for item in self._statements:
            data = data + f"{item}"
            data = data + ""
        return data


class IfExpression(Expression):
    def __init__(self, token: Token,  # 'If' token
                 condition: Expression = None,
                 consequence: List[BlockStatement] = None,
                 alternative: List[BlockStatement] = None):
        self._token = token
        self._condition = condition
        self._consequence = consequence
        self._alternative = alternative

    def token_literal(self) -> str:
        return self._token.literal

    def expression_node(self):
        pass

    def __str__(self):
        data = f"{self._token.literal} {str(self._condition)} " + "{ " + str(self._consequence) + " }"

        if self._alternative:
            data = data + " else " + "{ " + str(self._alternative) + " }"

        return data


class FunctionLiteral(Expression):
    def __init__(self, token: Token, parameters: List[Identifier] = None,
                 block: BlockStatement = None):
        self._token = token  # The 'fn' token
        self._parameters = parameters
        self._block = block

    def token_literal(self) -> str:
        return self._token.literal

    def expression_node(self):
        pass

    def __str__(self):
        data = f"{self._token.literal}" + "( " + ", ".join(self._parameters) + " )" + str(self._block)
        return data


class CallExpression(Expression):
    def __init__(self, token: Token,
                 ident_or_func_literal: Expression = None, args: List[Expression] = None):
        self._token = token,  # The '(' token
        self._ident_or_func_literal = ident_or_func_literal
        self._args = args

    def token_literal(self) -> str:
        return self._token.literal

    def expression_node(self):
        pass

    def __str__(self):
        data = f"{str(self._ident_or_func_literal)}" + "(" + ", ".join(str(item) for item in self._args) + ")"
        return data


class Program:
    def __init__(self):
        self._statements: List = []

    def token_literal(self):
        if len(self._statements) > 0:
            return self._statements[0].token_literal()
        else:
            return ""

    def __str__(self):
        data = ""
        for item in self._statements:
            data = data + f"{str(item)}"
            data = data + ""

        return data
