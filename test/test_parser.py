from parser import Parser
from lexer.monkey_lexer import Lexer
from abstract.monkey_ast import Statement, LetStatement, ReturnStatement, \
    ExpressionStatement, Identifier, IntegerLiteral, PrefixExpression, InfixExpression, IfExpression, \
    FunctionLiteral, CallExpression
import pytest


@pytest.fixture()
def provide_return_data():
    return """
    return 5;
    return 16;
    return 993322;
    """


@pytest.mark.parametrize("let_data", [("let foobar = add(2, 4);"),
                                      ("let y = true;"),
                                      ("let foobar = y;")])
def test_let_statements(let_data):
    lexer = Lexer(let_data)
    parser = Parser.new(lexer)
    program = parser.parse()

    if program is None:
        pytest.fail(f"Failed to process the input")

    if len(program._statements) != 1:
        pytest.fail(f"Mismatch: Expected -> 3 : Found -> {len(program._statements)}")

    assert let_data == str(program)


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


def assert_simple_identifier_expression_statement(statement, identifier_name):
    if not isinstance(statement, ExpressionStatement):
        return False

    if not isinstance(statement._expression, Identifier):
        return False

    if statement._expression._value != identifier_name:
        return False

    if statement._expression.token_literal() != identifier_name:
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

    assert assert_simple_identifier_expression_statement(program._statements[0], input)


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
                         expected_right_expression", [("!5;", "!", 5), ("-15;", "-", 15),
                                                      ("!True;", "!", "True"),
                                                      ("!False;", "!", "False"),
                                                      ])
def test_pratt_prefix_operators(input_data, expected_token_literal, expected_right_expression):
    lexer = Lexer(input_data)
    parser = Parser.new(lexer)
    program = parser.parse()

    check_parse_errors(parser)

    if len(program._statements) != 1:
        pytest.fail(f"Mismatch: Expected -> 1 : Found -> {len(program._statements)}")

    statement = program._statements[0]

    assert assert_simple_prefix_operator_statement(statement, expected_token_literal, str(expected_right_expression))


def assert_simple_infix_operator_statement(statement, expected_left, expected_op, expected_right):
    if not isinstance(statement, ExpressionStatement):
        return False

    if not isinstance(statement._expression, InfixExpression):
        return False

    if str(statement._expression._left) != expected_left:
        return False

    if statement._expression._op != expected_op:
        return False

    if str(statement._expression._right) != expected_right:
        return False

    return True


@pytest.mark.parametrize("input_data, expected_left, expected_op,\
                         expected_right", [("5 + 5;", 5, "+", 5),
                                           ("5 - 5;", 5, "-", 5),
                                           ("5 * 5;", 5, "*", 5),
                                           ("5 / 5;", 5, "/", 5),
                                           ("5 > 5;", 5, ">", 5),
                                           ("5 < 5;", 5, "<", 5),
                                           ("5 == 5;", 5, "==", 5),
                                           ("5 != 5;", 5, "!=", 5),
                                           ("True == True;", "True", "==", "True"),
                                           ("True != False;", "True", "!=", "False"),
                                           ("False == False;", "False", "==", "False")
                                           ])
def test_pratt_infix_operators(input_data, expected_left, expected_op, expected_right):
    lexer = Lexer(input_data)
    parser = Parser.new(lexer)
    program = parser.parse()

    check_parse_errors(parser)

    if len(program._statements) != 1:
        pytest.fail(f"Mismatch: Expected -> 1 : Found -> {len(program._statements)}")

    statement = program._statements[0]

    assert assert_simple_infix_operator_statement(statement, str(expected_left), expected_op, str(expected_right))


@pytest.mark.parametrize("input_data, expected_str", [("(1 + 2);", "(1 + 2)"),
                                                      ("1 + (2 + 3) + 4;", "((1 + (2 + 3)) + 4)"),
                                                      ("2 / (5 + 5);", "(2 / (5 + 5))"),
                                                      ("-(5 + 5);", "(-(5 + 5))"),
                                                      ("(5 + 5) * 2;", "((5 + 5) * 2)"),
                                                      # ("True;", "True"),
                                                      # ("3 > 5 == False;", "((3 > 5) == False)"),
                                                      # ("3 < 5 == True;", "((3 < 5) == True)"),
                                                      # ("-a * b;", "((-a) * b)"),
                                                      # ("!-a;", "(!(-a))"),
                                                      # ("a + b + c;", "((a + b) + c)"),
                                                      # ("a + b - c;", "((a + b) - c)"),
                                                      # ("a * b * c;", "((a * b) * c)"),
                                                      # ("a * b / c;", "((a * b) / c)"),
                                                      # ("a + b / c;", "(a + (b / c))"),
                                                      # ("a + b * c + d / e - f;", "(((a + (b * c)) + (d / e)) - f)"),
                                                      # ("3 + 4; -5 * 5;", "(3 + 4)((-5) * 5)"),
                                                      # ("5 > 4 == 3 < 4;", "((5 > 4) == (3 < 4))"),
                                                      # ("5 < 4 != 3 > 4;", "((5 < 4) != (3 > 4))"),
                                                      # ("3 + 4 * 5 == 3 * 1 + 4 * 5;", "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))")
                                                      ])
def test_operator_precedence_parsing(input_data, expected_str):
    lexer = Lexer(input_data)
    parser = Parser.new(lexer)
    program = parser.parse()

    check_parse_errors(parser)
    print(str(program))
    assert str(program).rstrip(" ") == expected_str


def test_if_expression():
    lexer = Lexer("if (x < y) { x } else { y }")
    parser = Parser.new(lexer)
    program = parser.parse()
    check_parse_errors(parser)

    if len(program._statements) != 1:
        pytest.fail(f"Mismatch: Expected -> 1 : Found -> {len(program._statements)}")

    statement = program._statements[0]

    assert isinstance(statement, ExpressionStatement), f"type mismatch {type(statement)}"

    if not isinstance(statement._expression, IfExpression):
        pytest.fail(f"Type mismatch:Got {type(statement._expression)}")

    assert str(program) == "if (x < y) { x } else { y }"


def test_function_literal():
    lexer = Lexer("fn(x, y) { x + y }")
    parser = Parser.new(lexer)
    program = parser.parse()
    check_parse_errors(parser)

    if len(program._statements) != 1:
        pytest.fail(f"Mismatch: Expected -> 1 : Found -> {len(program._statements)}")

    statement = program._statements[0]

    if not isinstance(statement._expression, FunctionLiteral):
        pytest.fail(f"Expected function literal : Found => {type(statement._expression)}")

    if len(statement._expression._parameters) != 2:
        pytest.fail(f"Expected two parameters : Got {len(statement._expression_parameters)}")

    assert statement._expression._parameters[0]._value == "x"
    assert statement._expression._parameters[1]._value == "y"

    assert str(statement._expression._block) == "(x + y)"


def test_call_expression():
    lexer = Lexer("add(1, 2 * 3, 4 + 5);")
    parser = Parser.new(lexer)
    program = parser.parse()
    check_parse_errors(parser)

    if len(program._statements) != 1:
        pytest.fail(f"Mismatch: Expected -> 1 : Found -> {len(program._statements)}")

    statement = program._statements[0]

    if not isinstance(statement, ExpressionStatement):
        pytest.fail(f"Expected ExpressionStatement : Got {type(statement)} instead")

    if not isinstance(statement._expression, CallExpression):
        pytest.fail(f"Expected Call Expression : Got => {type(statement._expression)}")

    if len(statement._expression._args) != 3:
        pytest.fail(f"Expected two parameters : Got {len(statement._expression._args)}")

    assert str(statement._expression._ident_or_func_literal) == "add"

    assert str(statement._expression._args[0]) == '1'
    assert str(statement._expression._args[1]) == '(2 * 3)'
