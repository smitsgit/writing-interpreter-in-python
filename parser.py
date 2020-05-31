from monkey_lexer import Lexer, Token, TokenTypes, TokenType
from monkey_ast import Program, LetStatement, Identifier, ReturnStatement, PrefixExpression, InfixExpression
from monkey_ast import Expression, ExpressionStatement, IntegerLiteral
from typing import Optional, Dict, Callable
from enum import Enum
from trace_helper import TraceCalls


class Precedence(Enum):
    LOWEST = 1,
    EQUALS = 2,
    LESS_GREATER = 3,
    SUM = 4,  # + -
    PRODUCT = 5,  # * /
    PREFIX = 6,
    CALL = 7


token_to_precedence = {
    TokenTypes.EQ: Precedence.EQUALS,
    TokenTypes.NOT_EQ: Precedence.EQUALS,
    TokenTypes.LT: Precedence.LESS_GREATER,
    TokenTypes.GT: Precedence.LESS_GREATER,
    TokenTypes.PLUS: Precedence.SUM,
    TokenTypes.MINUS: Precedence.SUM,
    TokenTypes.SLASH: Precedence.PRODUCT,
    TokenTypes.ASTERISK: Precedence.PRODUCT
}


class Parser:
    def __init__(self, lexer: Lexer, cur_token: Token = None,
                 peek_token: Token = None):
        self._lexer = lexer
        self._cur_token = cur_token
        self._peek_token = peek_token
        self.prefix_parsers: Dict[Token, Callable[[], Expression]] = {}
        self.infix_parsers: Dict[Token, Callable[[Expression], Expression]] = {}
        self.errors = []

    @classmethod
    def new(cls, lexer: Lexer):
        parser = Parser(lexer)

        # read two tokens so that current and peek tokens are set
        parser.next_token()
        parser.next_token()

        parser.register_prefix(TokenTypes.MINUS, parser.parse_prefix_expression)
        parser.register_prefix(TokenTypes.BANG, parser.parse_prefix_expression)
        parser.register_prefix(TokenTypes.IDENT, parser.parse_identifier)
        parser.register_prefix(TokenTypes.INT, parser.parse_integer)

        parser.register_infix(TokenTypes.PLUS, parser.parse_infix_expression)
        parser.register_infix(TokenTypes.MINUS, parser.parse_infix_expression)
        parser.register_infix(TokenTypes.LT, parser.parse_infix_expression)
        parser.register_infix(TokenTypes.GT, parser.parse_infix_expression)
        parser.register_infix(TokenTypes.SLASH, parser.parse_infix_expression)
        parser.register_infix(TokenTypes.ASTERISK, parser.parse_infix_expression)
        parser.register_infix(TokenTypes.EQ, parser.parse_infix_expression)
        parser.register_infix(TokenTypes.NOT_EQ, parser.parse_infix_expression)
        return parser

    def register_prefix(self, token: TokenTypes, func: Callable[[], Expression]):
        self.prefix_parsers[token] = func

    def register_infix(self, token: TokenTypes, func: Callable[[Expression], Expression]):
        self.infix_parsers[token] = func

    def next_token(self):
        self._cur_token = self._peek_token
        self._peek_token = self._lexer.next_token()

    def parse(self) -> Program:
        program = Program()

        while not self.current_token_is(TokenTypes.EOF):
            statement = self.parse_statement()
            if statement:
                program._statements.append(statement)

            self.next_token()

        return program

    def parse_let_statement(self):
        token = self._cur_token

        if not self.peek_token_is(TokenTypes.IDENT):
            return None

        self.next_token()
        name = self.parse_identifier()

        if not self.peek_token_is(TokenTypes.ASSIGN):
            return None

        statement = LetStatement(token, name)

        # We are not consuming value in let x = [ 5 ]; cause that
        # can be an expression and we are yet to see expression parsing
        while not self.current_token_is(TokenTypes.SEMICOLON):
            self.next_token()
        return statement

    def current_token_is(self, type: TokenType):
        return self._cur_token.type == type

    def peek_token_is(self, type: TokenType):
        return self._peek_token.type == type

    def parse_statement(self) -> Optional[LetStatement]:
        if self._cur_token.type == TokenTypes.LET:
            return self.parse_let_statement()
        if self._cur_token.type == TokenTypes.RETURN:
            return self.parse_return_statement()
        else:
            return self.parse_expression_statement()

    def parse_identifier(self):
        return Identifier(self._cur_token, self._cur_token.literal)

    def parse_integer(self):
        return IntegerLiteral(self._cur_token, int(self._cur_token.literal))

    def parse_return_statement(self):
        token = self._cur_token

        self.next_token()
        # TODO: We're skipping the expressions until we encounter a semicolon
        while not self.current_token_is(TokenTypes.SEMICOLON):
            self.next_token()

        return ReturnStatement(token)

    @TraceCalls()
    def parse_expression_statement(self):
        statement = ExpressionStatement(self._cur_token)
        statement._expression = self.parseExpression(Precedence.LOWEST.value)

        if self.peek_token_is(TokenTypes.SEMICOLON):
            self.next_token()

        return statement

    @TraceCalls()
    def parse_prefix_expression(self):
        expression = PrefixExpression(self._cur_token, self._cur_token.literal)
        self.next_token()
        expression._right = self.parseExpression(Precedence.PREFIX.value)
        return expression

    @TraceCalls()
    def parse_infix_expression(self, left: Expression):
        expression = InfixExpression(self._cur_token, self._cur_token.literal, left=left)
        precedence = self.curr_precedence()
        self.next_token()
        expression._right = self.parseExpression(precedence)
        return expression

    @TraceCalls()
    def parseExpression(self, precedence):
        """
        Whenever we wish to parse expression, check the token type,
        See if there is registered function to handle the current token type
        and call that function
        :return:
        """
        prefix_fn = self.prefix_parsers.get(self._cur_token.type, None)
        if prefix_fn:
            left_exp = prefix_fn()
        else:
            self.errors.append(f"No Prefix Parser not found to for token type : {self._cur_token}")
            return None

        while self._cur_token.type != TokenTypes.SEMICOLON and \
                precedence < self.peek_precedence():

            infix_fn = self.infix_parsers.get(self._peek_token.type, None)
            if infix_fn is None:
                return left_exp

            self.next_token()
            left_exp = infix_fn(left_exp)

        return left_exp

    def peek_precedence(self) -> int:
        return token_to_precedence.get(self._peek_token.type, Precedence.LOWEST).value

    def curr_precedence(self) -> int:
        return token_to_precedence.get(self._cur_token.type, Precedence.LOWEST).value
