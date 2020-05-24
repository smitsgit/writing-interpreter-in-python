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
    EQUALS = "="

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


class Lexer:
    def __init__(self, input: str):
        self._input = input
        self.position = -1
        self.read_position = self.position + 1
        self.chr = None

    def next_token(self) -> Token:
        if self.read_position <= len(self._input) != 0:
            self.chr = self._input[self.read_position]
        else:
            self.chr = 0

        self.position = self.read_position
        self.read_position += 1

        if self.chr == '=':
            return Token(TokenTypes.EQUALS, "=")
        if self.chr == '+':
            return Token(TokenTypes.PLUS, "+")
        if self.chr == '(':
            return Token(TokenTypes.LPAREN, "(")
        if self.chr == ')':
            return Token(TokenTypes.RPAREN, ")")
        if self.chr == '{':
            return Token(TokenTypes.LBRACE, "{")
        if self.chr == '}':
            return Token(TokenTypes.RBRACE, "}")
        if self.chr == ',':
            return Token(TokenTypes.COMMA, ",")
        if self.chr == ';':
            return Token(TokenTypes.SEMICOLON, ";")
        if self.chr == 0:
            return Token(TokenTypes.EOF, "")
