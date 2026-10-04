from toolkit.errors import MissingOperatorError, InvalidCharacterError, EmptyExpressionError, \
    InvalidCharacterAfterDotError, MissingOperandError, TwoOperatorsError


def tokenize_fsm(expr: str) -> list:
    if '$' in expr:
        raise InvalidCharacterError('неизвестный символ $')
    expr = expr.replace('//', '$')
    tokens = []
    state = 'START'
    current_token = ''
    operators = ['*','/','%','$','+','-'] # заменил // на $ чтобы // не путался с /
    if len(expr) == 0:
        raise EmptyExpressionError('Пусто')
    for char in expr:
        if state == 'START':
            if char.isdigit():
                state = 'NUMBER'
                current_token = char
            elif char in '+-':
                state = 'UNARY_OPERATOR'
                current_token = char
            elif char.isspace():
                continue
            elif char in operators:
                raise MissingOperandError(f'Пропущен операнд перед {char}')
            else:
                raise InvalidCharacterError(f'неизвестный символ {char}')

        elif state == 'NUMBER':
            if char.isdigit():
                current_token += char
            elif char == '.' and '.' not in current_token:
                state = 'DOT'
                current_token += char
            elif char in operators:
                tokens.append(('NUMBER', float(current_token)))
                current_token = char
                state = 'OPERATOR'
            elif char.isspace():
                state = 'SPACE_AFTER_NUM'
            else:
                raise InvalidCharacterError(f'неизвестный символ {char}')


        elif state == 'SPACE_AFTER_NUM':
            if char.isdigit():
                raise MissingOperatorError(f'Пропущен оператор перед {char}')
            elif char in operators:
                tokens.append(('NUMBER',float(current_token)))
                current_token = char
                state = 'OPERATOR'
            elif char.isspace():
                continue
            else:
                raise InvalidCharacterError(f'неизвестный символ {char}')


        elif state == 'DOT':
            if char.isdigit():
                current_token += char
                state = 'NUMBER'
            else:
                raise InvalidCharacterAfterDotError(f'неизвестный символ {char}')


        elif state == 'OPERATOR':
            if char.isdigit():
                tokens.append(('OPERATOR',current_token))
                current_token = char
                state = 'NUMBER'
            elif char in '+-':
                tokens.append(('OPERATOR',current_token))
                current_token = char
                state = 'UNARY_OPERATOR'
            elif char in operators:
                raise TwoOperatorsError('два бинарных оператора подряд')
            elif char.isspace():
                continue
            else:
                raise InvalidCharacterError(f'неизвестный символ {char}')

        elif state == 'UNARY_OPERATOR':
            if char.isdigit():
                current_token += char
                state = 'NUMBER'
            elif char.isspace():
                continue
            elif char in operators:
                raise TwoOperatorsError('два бинарных оператора подряд')
            else:
                raise InvalidCharacterError(f'неизвестный символ {char}')


    # Завершающая обработка
    if state in ('NUMBER', 'SPACE_AFTER_NUM'):
        tokens.append(('NUMBER', float(current_token)))
    elif state in ('OPERATOR', 'UNARY_OPERATOR'):
        raise MissingOperandError('Выражение заканчивается оператором')
    elif state == 'DOT':
        raise InvalidCharacterAfterDotError('Число заканчивается точкой')
    elif state == 'START':
        raise EmptyExpressionError('Пусто')

    return back_to_base_operator(tokens)

def back_to_base_operator(tokens: list) -> list: # возвращаем обратно опреатор //
    based_tokens = []
    for state,char in tokens:
        if char == '$':
            based_tokens.append((state,'//'))
        else:
            based_tokens.append((state,char))
    return based_tokens