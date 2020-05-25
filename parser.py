from monkey_lexer import Lexer, Token
from ast import Program


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

    def next_token(self):
        self._cur_token = self._peek_token
        self._peek_token = self._lexer.next_token()

    def parse(self) -> Program:
        return None
