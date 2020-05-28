from interface import implements, Interface
from typing import List
from monkey_lexer import Token, TokenTypes


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


class LetStatement(Statement):
    def __init__(self, token: Token, name: Identifier, value: Expression = None):
        self._token = token  # TokenTypes.LET token
        self._name = name
        self._value = value

    def token_literal(self) -> str:
        return self._token.literal

    def statement_node(self):
        pass

    def __str__(self):
        repr = f"{self.token_literal()} {self._name} ="
        if self._value:
            repr = repr + f"{self._value};"

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

        return "### No Repr ####"


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
            data = data + f"{item}"
            data = data + "\n"

        return data
