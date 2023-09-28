import time

def is_accepted(afn, input_string):
        start = time.time()
        def epsilon_closure(states):
            ec = set(states)
            stack = list(states)
            while stack:
                current_state = stack.pop()
                if (current_state, 'ε') in afn.transitions:
                    for next_state in afn.transitions[(current_state, 'ε')]:
                        if next_state not in ec:
                            ec.add(next_state)
                            stack.append(next_state)
            return ec

        current_states = epsilon_closure({afn.initial_state})

        for symbol in input_string:
            print(f'Estados actuales: {current_states}')
            next_states = set()
            for state in current_states:
                if (state, symbol) in afn.transitions:
                    next_states.update(afn.transitions[(state, symbol)])
                    print(f'{(state, symbol)}: {afn.transitions[(state, symbol)]}')
            current_states = epsilon_closure(next_states)

        if any(state == afn.final_state for state in current_states):
          print(f'La cadena {input_string} sí es aceptada por el AFN. Tiempo transcurrido {time.time() - start} s.')
        else:
           raise ValueError(f'La cadena {input_string} no es aceptada por el AFN. Tiempo transcurrido {time.time() - start} s.')
