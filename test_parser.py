from parser import Parser
from monkey_lexer import Lexer
from monkey_ast import Statement, LetStatement, ReturnStatement, \
    ExpressionStatement, Expression, Identifier, IntegerLiteral, PrefixExpression
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


def assert_simple_identifier_expression_statement(statement):
    if not isinstance(statement, ExpressionStatement):
        return False

    if not isinstance(statement._expression, Identifier):
        return False

    if statement._expression._value != "foobar":
        return False

    if statement._expression.token_literal() != "foobar":
        return False

    return True


def test_pratt_identifiers():
    input = "foobar;"

    lexer = Lexer(input)
    parser = Parser.new(lexer)
    program = parser.parse()

    if program is None:
        pytest.fail(f"Failed to process the input")

    if len(program._statements) != 1:
        pytest.fail(f"Mismatch: Expected -> 1 : Found -> {len(program._statements)}")

    assert assert_simple_identifier_expression_statement(program._statements[0])


def assert_simple_integer_expression(statement):
    if not isinstance(statement, ExpressionStatement):
        return False

    if not isinstance(statement._expression, IntegerLiteral):
        return False

    if statement._expression._value != 5:
        return False

    if statement._expression.token_literal() != "5":
        return False

    return True


def test_pratt_integer_literals():
    input = "5;"

    lexer = Lexer(input)
    parser = Parser.new(lexer)
    program = parser.parse()

    if program is None:
        pytest.fail(f"Failed to process the input")

    if len(program._statements) != 1:
        pytest.fail(f"Mismatch: Expected -> 1 : Found -> {len(program._statements)}")

    statement = program._statements[0]

    assert assert_simple_integer_expression(statement)


def check_parse_errors(parser):
    if len(parser.errors):
        for msg in parser.errors:
            print(msg)
        pytest.fail("Parser has encountered errors")


def assert_simple_prefix_operator_statement(statement, expected_token_literal, expected_right_expression):
    if not isinstance(statement, ExpressionStatement):
        return False

    if not isinstance(statement._expression, PrefixExpression):
        return False

    if statement._expression._op != expected_token_literal:
        return False

    if str(statement._expression._right) != expected_right_expression:
        return False

    return True


@pytest.mark.parametrize("input_data, expected_token_literal,\
                         expected_right_expression", [("!5;", "!", 5), ("-15;", "-", 15)])
def test_pratt_prefix_operators(input_data, expected_token_literal, expected_right_expression):
    lexer = Lexer(input_data)
    parser = Parser.new(lexer)
    program = parser.parse()

    check_parse_errors(parser)

    if len(program._statements) != 1:
        pytest.fail(f"Mismatch: Expected -> 1 : Found -> {len(program._statements)}")

    statement = program._statements[0]

    assert assert_simple_prefix_operator_statement(statement, expected_token_literal, str(expected_right_expression))