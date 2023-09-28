def state_lock(current_state, transitions):
    '''
        Cerradura de estados para un estado dado.
    '''
    lock = [current_state]
    for state in lock:
        for newState in [st for (key, value) in transitions.items() if key[0] == state and key[1] == 'ε' for st in value]:
            lock.append(newState)
    return set(lock)

def subsets(afn):
    '''
       Implementacion de algoritmo de construccion de subconjuntos.
    '''
    # Valores iniciales del AFD
    states = [state_lock(afn.initial_state, afn.transitions)]
    symbols = set([element[1] for element in afn.transitions if element[1] != 'ε'])
    acceptance = []
    transitions = []
    for state in states:
        for symbol in symbols:
            destination = {}
            for substate in state:
                locks = [state_lock(st, afn.transitions)
                         for (key, value) in afn.transitions.items()
                         if key[0] == substate and key[1] == symbol for st in value]
                destination = set().union(destination, *locks)
            if destination == set():
                destination = {}
            transitions.append((state,symbol,destination))
            if destination not in states:
                states.append(destination)
        if afn.final_state in state:
            acceptance.append(state)

    AFD = {
        'STATES': states,
        'SYMBOLS': symbols,
        'INITIAL_STATE': states[0],
        'ACCEPTANCE': acceptance,
        'TRANSITIONS': transitions
    }
    return AFD


