def hopcroft_minimization(afd):

  pairs_to_check = []

  # obtener parejas de terminales y no terminales
  for acceptance_state in afd['ACCEPTANCE']:
    for state in afd['STATES']:
      if(state not in afd['ACCEPTANCE']): pairs_to_check.append({str(acceptance_state), str(state)})

  count = 0
  while count < len(pairs_to_check):

    # Para cada simbolo, obtener las transiciones que dan como resultado a uno de los elementos
    # de la pareja

    for symbol in afd['SYMBOLS']:
      
      current_pair = list(pairs_to_check[count])
      first_element_transitions = [trans for trans in afd['TRANSITIONS'] if trans[1] == symbol and str(trans[2]) == current_pair[0]]
      second_element_transitions = [trans for trans in afd['TRANSITIONS'] if trans[1] == symbol and str(trans[2]) == current_pair[1]]

      # Realizar combinacion de todas las transiciones
      for first_transition in first_element_transitions:
        for second_transition in second_element_transitions:

          origin_pair = {str(first_transition[0]), str(second_transition[0])}

          # Verificar si alguna de las parejas compuesta por los nodos predecesores aún no ha sido agregada
          if origin_pair not in pairs_to_check:
            pairs_to_check.append(origin_pair)


    count += 1

  # obtener parejas que no están en la lista (parejas equivalentes)
  equal_pairs = []
  for state1 in afd['STATES']:
    for state2 in afd['STATES']:
      states_pair = {str(state1), str(state2)}
      if state1 != state2 and states_pair not in pairs_to_check and states_pair not in equal_pairs:
        equal_pairs.append(states_pair)


  # agrupar estados que son equivalentes
  result_states = []
  for equal_pair in equal_pairs:
    index = 0
    equivalent_state_found = False
    while index < len(result_states):

      current_equal_pair = list(equal_pair)
      # verificar si alguno de los pares está en los estados agrupados (serían iguales)
      if current_equal_pair[0] in result_states[index] or current_equal_pair[1] in result_states[index]:
        result_states[index].add(current_equal_pair[0])
        result_states[index].add(current_equal_pair[1])
        equivalent_state_found = True
        break

      index +=1
    
    if not equivalent_state_found:
      # No se agruparon con otros estados, añadir pareja a un nuevo conjunto
      result_states.append(equal_pair)

  #añadir el resto de estados
  for state in afd['STATES']:
    skip_state = False

    for added_state in result_states:
      if str(state) in added_state or str(state) == added_state:
        skip_state = True
        break

    if not skip_state:
      result_states.append({str(state)})

  #reemplazar estados en afd
  initial_state =  next((state for state in result_states if str(afd['INITIAL_STATE']) in state), None)
  acceptance_state = set(tuple(state) for acceptance in afd['ACCEPTANCE'] for state in result_states if str(acceptance) in state)
  transitions = list(afd['TRANSITIONS'])
  index = 0
  while index < len(transitions):

    current_transition = list(transitions[index])

    for state in result_states:
      
      if str(current_transition[0]) in state:
        current_transition[0] = state
      if str(current_transition[2]) in state:
        current_transition[2] = state

    transitions[index] = tuple(current_transition)
    index += 1
  
  transitions = set((tuple(x[0]), x[1], tuple(x[2])) for x in transitions)
  
  afd_min = {
        'STATES': [tuple(x) for x in result_states],
        'SYMBOLS': afd["SYMBOLS"],
        'INITIAL_STATE': tuple(initial_state),
        'ACCEPTANCE': acceptance_state,
        'TRANSITIONS': transitions
    }

  return afd_min
      

