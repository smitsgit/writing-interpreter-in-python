import pytest

from lexer.monkey_lexer import Lexer
from parser import Parser
from test.test_parser import check_parse_errors
from evaluator import eval


@pytest.mark.parametrize("input_data, expected_val", [("5;", 5),
                                                      ("10;", 10),
                                                      ("-5;", -5),
                                                      ("-10;", -10),
                                                      ("5 + 5 + 5 + 5 - 10;", 10),
                                                      ("2 * 2 * 2 * 2 * 2;", 32),
                                                      ("-50 + 100 + -50;", 0),
                                                      ("5 * 2 + 10;", 20),
                                                      ("5 + 2 * 10;", 25),
                                                      ("20 + 2 * -10;", 0),
                                                      ("50 / 2 * 2 + 10;", 60),
                                                      ("2 * (5 + 10);", 30),
                                                      ("3 * 3 * 3 + 10;", 37),
                                                      ("3 * (3 * 3) + 10;", 37),
                                                      ("(5 + 10 * 2 + 15 / 3) * 2 + -10;", 50),
                                                      ])
def test_eval_integer_expression(input_data, expected_val):
    lexer = Lexer(input_data)
    parser = Parser.new(lexer)
    program = parser.parse()
    check_parse_errors(parser)

    output = eval(program)
    assert output.value == expected_val


@pytest.mark.parametrize("input_data, expected_val", [
                                                      ("true;", True),
                                                      ("false;", False),
                                                      ("true == true;", True),
                                                      ("false == false;", True),
                                                      ("true == false;", False),
                                                      ("true != false;", True),
                                                      ("false != true;", True),
                                                      ("1 < 2;", True),
                                                      ("1 > 2;", False),
                                                      ("1 < 1;", False),
                                                      ("1 > 1;", False),
                                                      ("1 == 1;", True),
                                                      ("1 != 1;", False),
                                                      ("1 == 2;", False),
                                                      ("1 != 2;", True),
                                                      ])
def test_eval_boolean_expression(input_data, expected_val):
    lexer = Lexer(input_data)
    parser = Parser.new(lexer)
    program = parser.parse()
    check_parse_errors(parser)

    output = eval(program)
    if hasattr(output, "value"):
        assert output.value == expected_val
    else:
        assert output == expected_val


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