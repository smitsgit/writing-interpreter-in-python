import pytest

from lexer.monkey_lexer import Lexer
from parser import Parser
from test.test_parser import check_parse_errors
from evaluator import eval


@pytest.mark.parametrize("input_data, expected_val", [("5;", 5),
                                                      ("10;", 10),
                                                      ("-5;", -5),
                                                      ("-10;", -10)
                                                      ])
def test_eval_integer_expression(input_data, expected_val):
    lexer = Lexer(input_data)
    parser = Parser.new(lexer)
    program = parser.parse()
    check_parse_errors(parser)

    output = eval(program)
    assert output.value == expected_val


@pytest.mark.parametrize("input_data, expected_val", [("true;", True),
                                                      ("false;", False)
                                                      ])
def test_eval_boolean_expression(input_data, expected_val):
    lexer = Lexer(input_data)
    parser = Parser.new(lexer)
    program = parser.parse()
    check_parse_errors(parser)

    output = eval(program)
    assert output.value == expected_val


@pytest.mark.parametrize("input_data, expected_val", [
                                                      ("!true;", False),
                                                      ("!false;", True),
                                                      ("!!true;", True),
                                                      ("!!false;", False),
                                                      ("!5;", False)
                                                      ])
def test_bang_operator(input_data, expected_val):
    lexer = Lexer(input_data)
    parser = Parser.new(lexer)
    program = parser.parse()
    check_parse_errors(parser)

    output = eval(program)
    assert output.value == expected_val