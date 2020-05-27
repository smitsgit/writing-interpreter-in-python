from parser import Parser
from monkey_lexer import Lexer
from monkey_ast import Statement, LetStatement, ReturnStatement
import pytest


@pytest.fixture()
def provide_let_data():
    return """
     let x = 5;
    let y = 10;
    let foobar = 838383;
    """


@pytest.fixture()
def provide_return_data():
    return """
    return 5;
    return 16;
    return 993322;
    """


def test_let_statements(provide_let_data):
    lexer = Lexer(provide_let_data)
    parser = Parser.new(lexer)
    program = parser.parse()

    if program is None:
        pytest.fail(f"Failed to process the input")

    if len(program._statements) != 3:
        pytest.fail(f"Mismatch: Expected -> 3 : Found -> {len(program._statements)}")

    expected_identifier_names = ['x', 'y', 'foobar']

    for statement, expected_name in zip(program._statements, expected_identifier_names):
        assert assert_single_let_statement(statement, expected_name)


def assert_single_let_statement(statement: Statement, name: str):
    if statement.token_literal() != "let":
        return False

    if not isinstance(statement, LetStatement):
        return False

    if statement._name._value != name:
        return False

    if statement._name.token_literal() != name:
        return False

    return True


def assert_single_return_statement(statement):
    if not isinstance(statement, ReturnStatement):
        return False

    if statement.token_literal() != "return":
        return False

    return True


def test_return_statement(provide_return_data):
    lexer = Lexer(provide_return_data)
    parser = Parser.new(lexer)
    program = parser.parse()

    if program is None:
        pytest.fail(f"Failed to process the input")

    if len(program._statements) != 3:
        pytest.fail(f"Mismatch: Expected -> 3 : Found -> {len(program._statements)}")

    for statement in program._statements:
        assert assert_single_return_statement(statement)
