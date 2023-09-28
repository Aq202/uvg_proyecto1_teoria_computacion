class AFN:
    def __init__(self, symbol, current_state):
        self.initial_state = current_state
        self.final_state = current_state + 1
        self.transitions = {(current_state, symbol): [current_state + 1]}
        self.symbols = []
        self.states = []

def build_afn_from_postfix(postfix_expression):
    stack = []
    symbols = []
    current_state = 0

    for token in postfix_expression:
        if token.isalnum():
            if token not in symbols:
                symbols.append(token)
            afn = AFN(token, current_state)
            current_state += 2
            stack.append(afn)
        elif token == '.':
            afn2 = stack.pop()
            afn1 = stack.pop()
            afn1.transitions.update(afn2.transitions)
            for element in afn1.transitions:
                if afn1.final_state in afn1.transitions[element]:
                    afn1.transitions[element].remove(afn1.final_state)
                    afn1.transitions[element].append(afn2.initial_state)
            afn1.final_state = afn2.final_state
            stack.append(afn1)
        elif token == '|' or token == '+':
            afn2 = stack.pop()
            afn1 = stack.pop()
            afn = AFN('ε', current_state)
            current_state += 2
            afn.transitions = {(afn.initial_state, 'ε'): [afn1.initial_state, afn2.initial_state],
                                   (afn1.final_state, 'ε'): [afn.final_state],
                                   (afn2.final_state, 'ε'): [afn.final_state]}
            afn.transitions.update(afn1.transitions)
            afn.transitions.update(afn2.transitions)
            stack.append(afn)
        elif token == '*':
            afn1 = stack.pop()
            afn = AFN('ε', current_state)
            current_state += 2
            afn.transitions ={(afn.initial_state, 'ε'): [afn1.initial_state, afn.final_state],
                                   (afn1.final_state, 'ε'): [afn1.initial_state, afn.final_state]}
            afn.transitions.update(afn1.transitions)
            stack.append(afn)

    if len(stack) == 1:
        afn = stack[0]
        afn.symbols = symbols
        for state in afn.transitions.keys():
            if state[0] not in afn.states:
                afn.states.append(state[0])
        for element in afn.transitions.values():
            for state in element:
                if state not in afn.states:
                    afn.states.append(state)
        return afn
    else:
        raise ValueError("La expresión postfix no es válida")