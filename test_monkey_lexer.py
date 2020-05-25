from monkey_lexer import Lexer
from monkey_lexer import TokenTypes
from monkey_lexer import Token
import pytest


def test_lexer_returns_none_on_empty():
    lexer = Lexer("")
    assert lexer.next_token() == Token(TokenTypes.EOF, "")


def test_is_letter():
    lexer = Lexer("")
    assert lexer.is_letter('c')
    assert lexer.is_letter('*') is False
    assert lexer.is_letter('_')
    assert lexer.is_letter(' ') is False


def test_lexer_returns_correct_tokens():
    data = "=+(){},;"
    lexer = Lexer(data)

    assert lexer.next_token() == Token(TokenTypes.ASSIGN, "=")
    assert lexer.next_token() == Token(TokenTypes.PLUS, "+")
    assert lexer.next_token() == Token(TokenTypes.LPAREN, "(")
    assert lexer.next_token() == Token(TokenTypes.RPAREN, ")")
    assert lexer.next_token() == Token(TokenTypes.LBRACE, "{")
    assert lexer.next_token() == Token(TokenTypes.RBRACE, "}")
    assert lexer.next_token() == Token(TokenTypes.COMMA, ",")
    assert lexer.next_token() == Token(TokenTypes.SEMICOLON, ";")
    assert lexer.next_token() == Token(TokenTypes.EOF, "")


def test_lexer_parses_bare_monkey_syntax():
    data = "let five = 5;"
    lexer = Lexer(data)

    assert lexer.next_token() == Token(TokenTypes.LET, "let")
    assert lexer.next_token() == Token(TokenTypes.IDENT, "five")
    assert lexer.next_token() == Token(TokenTypes.ASSIGN, "=")
    assert lexer.next_token() == Token(TokenTypes.INT, "5")
    assert lexer.next_token() == Token(TokenTypes.SEMICOLON, ";")
    assert lexer.next_token() == Token(TokenTypes.EOF, "")


def test_lexer_parses_minimum_monkey_syntax():
    data = """let five = 5;
let ten = 10;
   let add = fn(x, y) {
     x + y;
};
   let result = add(five, ten);
   
   !-/*5;
   5 < 10 > 5;
   
   if (5 < 10) {
       return true;
   } else {
       return false;
   }
   
   10 == 10; 
   10 != 9;
   """

    lexer = Lexer(data)

    assert lexer.next_token() == Token(TokenTypes.LET, "let")
    assert lexer.next_token() == Token(TokenTypes.IDENT, "five")
    assert lexer.next_token() == Token(TokenTypes.ASSIGN, "=")
    assert lexer.next_token() == Token(TokenTypes.INT, "5")
    assert lexer.next_token() == Token(TokenTypes.SEMICOLON, ";")

    assert lexer.next_token() == Token(TokenTypes.LET, "let")
    assert lexer.next_token() == Token(TokenTypes.IDENT, "ten")
    assert lexer.next_token() == Token(TokenTypes.ASSIGN, "=")
    assert lexer.next_token() == Token(TokenTypes.INT, "10")
    assert lexer.next_token() == Token(TokenTypes.SEMICOLON, ";")

    assert lexer.next_token() == Token(TokenTypes.LET, "let")
    assert lexer.next_token() == Token(TokenTypes.IDENT, "add")
    assert lexer.next_token() == Token(TokenTypes.ASSIGN, "=")
    assert lexer.next_token() == Token(TokenTypes.FUNCTION, "fn")
    assert lexer.next_token() == Token(TokenTypes.LPAREN, "(")
    assert lexer.next_token() == Token(TokenTypes.IDENT, "x")
    assert lexer.next_token() == Token(TokenTypes.COMMA, ",")
    assert lexer.next_token() == Token(TokenTypes.IDENT, "y")
    assert lexer.next_token() == Token(TokenTypes.RPAREN, ")")
    assert lexer.next_token() == Token(TokenTypes.LBRACE, "{")
    assert lexer.next_token() == Token(TokenTypes.IDENT, "x")
    assert lexer.next_token() == Token(TokenTypes.PLUS, "+")
    assert lexer.next_token() == Token(TokenTypes.IDENT, "y")
    assert lexer.next_token() == Token(TokenTypes.SEMICOLON, ";")
    assert lexer.next_token() == Token(TokenTypes.RBRACE, "}")
    assert lexer.next_token() == Token(TokenTypes.SEMICOLON, ";")

    assert lexer.next_token() == Token(TokenTypes.LET, "let")
    assert lexer.next_token() == Token(TokenTypes.IDENT, "result")
    assert lexer.next_token() == Token(TokenTypes.ASSIGN, "=")
    assert lexer.next_token() == Token(TokenTypes.IDENT, "add")
    assert lexer.next_token() == Token(TokenTypes.LPAREN, "(")
    assert lexer.next_token() == Token(TokenTypes.IDENT, "five")
    assert lexer.next_token() == Token(TokenTypes.COMMA, ",")
    assert lexer.next_token() == Token(TokenTypes.IDENT, "ten")
    assert lexer.next_token() == Token(TokenTypes.RPAREN, ")")
    assert lexer.next_token() == Token(TokenTypes.SEMICOLON, ";")

    assert lexer.next_token() == Token(TokenTypes.BANG, "!")
    assert lexer.next_token() == Token(TokenTypes.MINUS, "-")
    assert lexer.next_token() == Token(TokenTypes.SLASH, "/")
    assert lexer.next_token() == Token(TokenTypes.ASTERISK, "*")
    assert lexer.next_token() == Token(TokenTypes.INT, "5")
    assert lexer.next_token() == Token(TokenTypes.SEMICOLON, ";")

    assert lexer.next_token() == Token(TokenTypes.INT, "5")
    assert lexer.next_token() == Token(TokenTypes.LT, "<")
    assert lexer.next_token() == Token(TokenTypes.INT, "10")
    assert lexer.next_token() == Token(TokenTypes.GT, ">")
    assert lexer.next_token() == Token(TokenTypes.INT, "5")
    assert lexer.next_token() == Token(TokenTypes.SEMICOLON, ";")

    # if (5 < 10) {
    # return true;
    # } else {
    # return false; }
    assert lexer.next_token() == Token(TokenTypes.IF, "if")
    assert lexer.next_token() == Token(TokenTypes.LPAREN, "(")
    assert lexer.next_token() == Token(TokenTypes.INT, "5")
    assert lexer.next_token() == Token(TokenTypes.LT, "<")
    assert lexer.next_token() == Token(TokenTypes.INT, "10")
    assert lexer.next_token() == Token(TokenTypes.RPAREN, ")")
    assert lexer.next_token() == Token(TokenTypes.LBRACE, "{")
    assert lexer.next_token() == Token(TokenTypes.RETURN, "return")
    assert lexer.next_token() == Token(TokenTypes.TRUE, "true")
    assert lexer.next_token() == Token(TokenTypes.SEMICOLON, ";")
    assert lexer.next_token() == Token(TokenTypes.RBRACE, "}")
    assert lexer.next_token() == Token(TokenTypes.ELSE, "else")
    assert lexer.next_token() == Token(TokenTypes.LBRACE, "{")
    assert lexer.next_token() == Token(TokenTypes.RETURN, "return")
    assert lexer.next_token() == Token(TokenTypes.FALSE, "false")
    assert lexer.next_token() == Token(TokenTypes.SEMICOLON, ";")
    assert lexer.next_token() == Token(TokenTypes.RBRACE, "}")

    assert lexer.next_token() == Token(TokenTypes.INT, "10")
    assert lexer.next_token() == Token(TokenTypes.EQ, "==")
    assert lexer.next_token() == Token(TokenTypes.INT, "10")
    assert lexer.next_token() == Token(TokenTypes.SEMICOLON, ";")

    assert lexer.next_token() == Token(TokenTypes.INT, "10")
    assert lexer.next_token() == Token(TokenTypes.NOT_EQ, "==")
    assert lexer.next_token() == Token(TokenTypes.INT, "9")
    assert lexer.next_token() == Token(TokenTypes.SEMICOLON, ";")
    assert lexer.next_token() == Token(TokenTypes.EOF, "")
