from monkey_ast import *
import pytest


@pytest.fixture()
def program():
    program = Program()
    statements = [
        LetStatement(Token(TokenTypes.LET, "let"), "myname", "5"),
        ReturnStatement(Token(TokenTypes.RETURN, "return"), "myname")
    ]
    program._statements = statements
    return program


def test_program_repr(program):
    print()
    data = f"{program}"
    assert data == "let myname =5;\nreturn myname;\n"
