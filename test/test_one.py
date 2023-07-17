import pytest
from one.main import evaluate_expression


#空的
def test_expression_none():
    expression = ""
    result = evaluate_expression(expression)
    assert result == "Invalid expression"


#有效
def test_expression_valid():
    expression = "2 + 3 * 4 - 1"
    expected_result = 13
    result = evaluate_expression(expression)
    assert result == expected_result


#加括號
def test_expression_brackets():
    expression = "(1+4) * (5-1)"
    expected_result = 20
    result = evaluate_expression(expression)
    assert result == expected_result


#單一數字
def test_expression_sigle_number():
    expression = "2"
    expected_result = 2
    result = evaluate_expression(expression)
    assert result == expected_result


#無效運算式
def test_expression_invalid():
    expression = "2 / 0"
    result = evaluate_expression(expression)
    assert result == "Invalid expression"


#無效的語法
def test_expression_invalid_syntax():
    expression = "2 +"
    result = evaluate_expression(expression)
    assert result == "Invalid expression"