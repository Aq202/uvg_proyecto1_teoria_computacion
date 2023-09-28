import time

def transition_afd(afd, q, a):
  transitions = afd['TRANSITIONS']
  for transition in transitions:
    if q == transition[0] and a == transition[1]:
      print(transition)
      return transition[2]
  raise ValueError("La cadena no es aceptada por el AFD.")

def derivation_afd(afd, w):
  print('\nComprobando cadena en AFD')
  start = time.time()
  current_state = afd['INITIAL_STATE']
  for char in w:
    current_state = transition_afd(afd, current_state, char)
  if current_state in afd['ACCEPTANCE']:
    print(f'La cadena {w} sí es aceptada por el AFD. Tiempo transcurrido {time.time() - start} s.')
  else:
    print(f'La cadena {w} no es aceptada por el AFD. Tiempo transcurrido {time.time() - start} s.')
