import time

def transition_afd_min(AFD_MIN, q, a):
  transitions = AFD_MIN['TRANSITIONS']
  for transition in transitions:
    if q == transition[0] and a == transition[1]:
      print(transition)
      return transition[2]

def derivation_afd_min(AFD_MIN, w):
  start = time.time()
  #print(AFD_MIN['INITIAL_STATE'])
  current_state = AFD_MIN['INITIAL_STATE']
  for char in w:
    current_state = transition_afd_min(AFD_MIN, current_state, char)
  if current_state in AFD_MIN['ACCEPTANCE']:
    print(f'La cadena {w} sí es aceptada por el AFD minimal. Tiempo transcurrido {time.time() - start} s.')
  else:
    print(f'La cadena {w} no es aceptada por el AFD minimal. Tiempo transcurrido {time.time() - start} s.')
