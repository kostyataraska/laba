from toolkit.calculating import calculating

def rpn_calculation(tokens):
    result  = []
    for state,char in tokens:
        if state == 'NUMBER':
            result.append(char)
        elif state == 'OPERATOR':
            calculating(result, char)
    return result[0]