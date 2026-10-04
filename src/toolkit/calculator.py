from toolkit.tokenezation import tokenize_fsm
from toolkit.RPN import rpn
from toolkit.RPN_calculation import rpn_calculation

def calculator(expression):
    return rpn_calculation(rpn(tokenize_fsm(expression)))
