"""
This is the input given to lexer

let x = 5 + 5;
We expect it to give us
[
LET,
IDENTIFIER("x"),
EQUAL SIGN,
INTEGER(5),
PLUS_SIGN,
INTEGER(5),
SEMICOLON
]

Observation:
whitespace characters don't show up as tokens

In our case length of the white space doesn't matter to us and it merely acts as separator
of the tokens

But in languages in Python, length of the whitespace does matter and lexer can't just eat
up the whitespace and newline and has to output them as the tokens so that parser in the later
stage can make sense out of it [ like throw error when there are too few or too many

Note:
    A production ready lexer might also contain the line no , file name and coloumn no to provide us
    useful message when the lexing goes wrong.

    "error: expected semicolon token. line 42, column 23, program.monkey"
"""
from pydantic import BaseModel
from pydantic.dataclasses import dataclass


class TokenType(str):
    pass


@dataclass
class Token:
    type: TokenType
    literal: str


class TokenTypes:
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    # Identifier and literals
    IDENT = "IDENT"
    INT = "INT"

    # operators
    PLUS = "+"
    MINUS = "-"
    ASSIGN = "="
    BANG = "!"
    ASTERISK = "*"
    SLASH = "/"
    LT = "<"
    GT = ">"
    EQ = "=="
    NOT_EQ = "!="

    # Delimiters
    COMMA = ","
    SEMICOLON = ";"

    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    # keywords
    LET = "LET"
    FUNCTION = "FUNCTION"
    FALSE = "FALSE"
    TRUE = "TRUE"
    IF = "IF"
    ELSE = "ELSE"
    RETURN = "RETURN"


keywords = {
    "let": Token(TokenTypes.LET, "let"),
    "fn": Token(TokenTypes.FUNCTION, "fn"),
    "true": Token(TokenTypes.TRUE, "true"),
    "false": Token(TokenTypes.FALSE, "false"),
    "if": Token(TokenTypes.IF, "if"),
    "else": Token(TokenTypes.ELSE, "else"),
    "return": Token(TokenTypes.RETURN, "return"),
}


class Lexer:
    def __init__(self, input: str):
        self._input = input
        self.position = -1
        self.read_position = self.position + 1
        self.chr = None

    def next_token(self) -> Token:
        self.skipNone()
        self.skip_whitespace()
        tok: TokenType = None
        if self.chr == '=':
            if self.peek_chr() == '=':
                self.read_chr()
                tok = Token(TokenTypes.EQ, "==")
            else:
                tok = Token(TokenTypes.ASSIGN, self.chr)
        elif self.chr == '+':
            tok = Token(TokenTypes.PLUS, self.chr)
        elif self.chr == '-':
            tok = Token(TokenTypes.MINUS, self.chr)
        elif self.chr == '(':
            tok = Token(TokenTypes.LPAREN, self.chr)
        elif self.chr == ')':
            tok = Token(TokenTypes.RPAREN, self.chr)
        elif self.chr == '{':
            tok = Token(TokenTypes.LBRACE, self.chr)
        elif self.chr == '}':
            tok = Token(TokenTypes.RBRACE, self.chr)
        elif self.chr == ',':
            tok = Token(TokenTypes.COMMA, self.chr)
        elif self.chr == ';':
            tok = Token(TokenTypes.SEMICOLON, self.chr)
        elif self.chr == '!':
            if self.peek_chr() == '=':
                self.read_chr()
                tok = Token(TokenTypes.NOT_EQ, "==")
            else:
                tok = Token(TokenTypes.BANG, self.chr)
        elif self.chr == '*':
            tok = Token(TokenTypes.ASTERISK, self.chr)
        elif self.chr == '/':
            tok = Token(TokenTypes.SLASH, self.chr)
        elif self.chr == '<':
            tok = Token(TokenTypes.LT, self.chr)
        elif self.chr == '>':
            tok = Token(TokenTypes.GT, self.chr)
        elif self.chr == 0:
            tok = Token(TokenTypes.EOF, "")
        else:
            if self.is_letter(self.chr):
                identifier = self.read_identifier()
                if identifier in keywords:
                    return keywords[identifier]
                else:
                    return Token(TokenTypes.IDENT, identifier)
            elif self.is_number(self.chr):
                number = self.read_num()
                return Token(TokenTypes.INT, number)
            else:
                return Token(TokenTypes.ILLEGAL, self.chr)
        self.read_chr()
        return tok

    def read_chr(self):
        if self.read_position < len(self._input) != 0:
            self.chr = self._input[self.read_position]
        else:
            self.chr = 0
        self.position = self.read_position
        self.read_position += 1

    def peek_chr(self) -> str:
        if self.read_position < len(self._input) != 0:
            chr = self._input[self.read_position]
        else:
            chr = 0
        return chr

    def read_identifier(self) -> str:
        position = self.position
        while True:
            if self.is_letter(self.chr):
                self.read_chr()
                continue
            else:
                break

        return self._input[position: self.position]

    def skip_whitespace(self):
        while self.chr in [' ', '\t', '\n', '\r']:
            self.read_chr()

    def is_letter(self, chr: str) -> bool:
        return 'a' <= chr <= 'z' or 'A' <= chr <= 'Z' or chr == '_'

    def is_number(self, chr: str) -> bool:
        return chr.isdigit()

    def read_num(self):
        position = self.position
        while True:
            if self.is_number(self.chr):
                self.read_chr()
                continue
            else:
                break
        return self._input[position: self.position]

    def skipNone(self):
        if self.chr is None:
            self.read_chr()

    def __iter__(self):
         return self

    def __next__(self):
        tok = self.next_token()
        if tok == Token(TokenTypes.EOF, ""):
            raise StopIteration
        return tok
