from toolkit.errors import DivisionByZeroError


def calculating(numbers,operator):
    if operator == '+':
        num1, num2 = numbers.pop(-2),numbers.pop(-1)
        numbers.append(num1+num2)
    elif operator == '-':
        num1, num2 = numbers.pop(-2),numbers.pop(-1)
        numbers.append(num1-num2)
    elif operator == '*':
        num1, num2 = numbers.pop(-2),numbers.pop(-1)
        numbers.append(num1*num2)
    elif operator == '/':
        num1, num2 = numbers.pop(-2),numbers.pop(-1)
        if num2 == 0.0:
            raise DivisionByZeroError('Деление на ноль запрещено!!!')
        else:
            numbers.append(num1/num2)
    elif operator == '%':
        num1, num2 = numbers.pop(-2), numbers.pop(-1)
        if num2 == 0.0:
            raise DivisionByZeroError('Деление на ноль запрещено!!!')
        else:
            numbers.append(num1%num2)
    elif operator == '//':
        num1, num2 = numbers.pop(-2),numbers.pop(-1)
        if num2 == 0.0:
            raise DivisionByZeroError('Деление на ноль запрещено!!!')
        else:
            numbers.append(num1//num2)
    return numbers