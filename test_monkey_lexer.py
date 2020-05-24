from monkey_lexer import Lexer
from monkey_lexer import TokenTypes
from monkey_lexer import Token
import pytest


def test_lexer_returns_none_on_empty():
    lexer = Lexer("")
    assert lexer.next_token() == Token(TokenTypes.EOF, "")


def test_lexer_returns_correct_tokens():
    data = "=+(){},;"
    lexer = Lexer(data)

    assert lexer.next_token() == Token(TokenTypes.EQUALS, "=")
    assert lexer.next_token() == Token(TokenTypes.PLUS, "+")
    assert lexer.next_token() == Token(TokenTypes.LPAREN, "(")
    assert lexer.next_token() == Token(TokenTypes.RPAREN, ")")
    assert lexer.next_token() == Token(TokenTypes.LBRACE, "{")
    assert lexer.next_token() == Token(TokenTypes.RBRACE, "}")
    assert lexer.next_token() == Token(TokenTypes.COMMA, ",")
    assert lexer.next_token() == Token(TokenTypes.SEMICOLON, ";")
