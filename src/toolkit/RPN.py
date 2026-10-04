PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, '%':2, '//':2}


def higher_or_equal(op1, op2):
    """True, если приоритет op1 >= op2"""
    return PRECEDENCE[op1] >= PRECEDENCE[op2]

def rpn(tokens):
    result = []
    stek_op = []
    for state,char in tokens:
        if state == 'NUMBER':
            result.append((state, char))
        elif state == 'OPERATOR':
            while len(stek_op) > 0 and higher_or_equal(stek_op[-1], char):
                result.append(('OPERATOR', stek_op.pop()))
            stek_op.append(char)
    while len(stek_op) > 0:
        result.append(('OPERATOR', stek_op.pop()))
    return result