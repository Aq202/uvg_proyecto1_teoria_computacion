"""
Algoritmo de Shunting Yard
Programado por:

Diego Morales Aquino - 21762
Erick Guerra Muñoz - 21781
Pablo Zamora Vásquez - 21780

"""

LEFT_ASSOCIATIVITY = 'LEFT'
RIGHT_ASSOCIATIVITY = 'RIGHT'
EMPTY_TOKEN = "ε"

operators = {'*': (2, LEFT_ASSOCIATIVITY),
             '.': (1, LEFT_ASSOCIATIVITY),
             '|': (0, RIGHT_ASSOCIATIVITY),
             '+': (0, RIGHT_ASSOCIATIVITY)
             }


def add_implicit_concatenations(regex):

    def is_not_operator(
        val): return val not in operators.keys() and val not in "()"

    index = 0
    new_regex = regex
    while(index < len(new_regex) - 1):  # Parar en el penultimo valor

        consecutive_symbols = is_not_operator(
            new_regex[index]) and is_not_operator(new_regex[index + 1])
        
        consecutive_symbols_and_parentheses = (is_not_operator(new_regex[index]) and new_regex[index + 1] == "(") or (
            new_regex[index] == ")" and is_not_operator(new_regex[index + 1]))
        
        consecutive_parentheses = new_regex[index] == ")" and new_regex[index + 1] == "("

        consecutive_klene_star = new_regex[index] == "*" and (
            is_not_operator(new_regex[index + 1]) or new_regex[index + 1] == '(')

        if consecutive_symbols or consecutive_symbols_and_parentheses or consecutive_parentheses or consecutive_klene_star:
            # Hay dos valores, valor y paréntesis, paréntesis adjayecentes o estrella de kleene y valor o paréntesis
            # añadir .
            new_regex = new_regex[0:index + 1] + '.' + \
                new_regex[index + 1: len(new_regex) + 1]
            index += 2
        else:
            index += 1
    return new_regex


def sunting_yard(regex):

    out = []
    operators_stack = []

    for token in regex:

        if token not in operators.keys() and token not in "()":
            # si el token es un valor, agregar a la cola de salida
            out.append(token)

        elif token != ")":

            if len(operators_stack) != 0:

                first_stack_operator = operators_stack[0]

                if token != "(" and first_stack_operator != "(" and (
                        (operators[token][1] == LEFT_ASSOCIATIVITY and operators[token][0] <= operators[first_stack_operator][0]) or (
                        operators[token][1] == RIGHT_ASSOCIATIVITY and operators[token][0] < operators[first_stack_operator][0])):

                    # es asociativo izquierdo y token 1 tiene menor o igual precedencia que el token 2 de la pila
                    # o es asociativo derecho y el token 1 tiene menor precedencia que el token 2 de la pila

                    # retirar token de la pila y colocarlo en out
                    out.append(operators_stack.pop(0))

            # Si es un operador colocarlo en la pila
            operators_stack.insert(0, token)
        else:
            # el token es: )
            operator_value = None
            while operator_value != "(":
                try:
                    # retirar tokens hasta encontrar (
                    operator_value = operators_stack.pop(0)
                    if operator_value != "(":
                        # si no es ( añadirlo a la salida
                        out.append(operator_value)
                except IndexError:
                    raise Exception(
                        "La expresión es inválida. Revise los paréntesis.")

    # retirar operadores restantes y añadirlos a la salida
    for remaining_operator in operators_stack:
        if remaining_operator == "(":
            raise Exception("La expresión es inválida. Revise los paréntesis.")

        out.append(remaining_operator)

    return out


if __name__ == "__main__":

    try:
        infix = input("Ingresa la regexp en formato infix: ")
        infix_with_concatenations = add_implicit_concatenations(infix)
        print(infix_with_concatenations)
        result_postfix = sunting_yard(infix_with_concatenations)
        print(
            f"El resultado de la cadena {infix} en formato infix a postfix es: \n{''.join(result_postfix)}")
    except Exception as ex:
        print(ex)
