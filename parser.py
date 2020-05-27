from monkey_lexer import Lexer, Token, TokenTypes, TokenType
from monkey_ast import Program, LetStatement, Identifier, ReturnStatement
from typing import Optional


class Parser:
    def __init__(self, lexer: Lexer, cur_token: Token = None,
                 peek_token: Token = None):
        self._lexer = lexer
        self._cur_token = cur_token
        self._peek_token = peek_token

    @classmethod
    def new(cls, lexer: Lexer):
        parser = Parser(lexer)

        # read two tokens so that current and peek tokens are set
        parser.next_token()
        parser.next_token()
        return parser

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
            return None

    def parse_identifier(self):
        return Identifier(self._cur_token, self._cur_token.literal)

    def parse_return_statement(self):
        token = self._cur_token

        self.next_token()
        # TODO: We're skipping the expressions until we encounter a semicolon
        while not self.current_token_is(TokenTypes.SEMICOLON):
            self.next_token()

        return ReturnStatement(token)
