from shunting_yard import *
from thompson import *
from subsets import *
from hopcroft_minimization import *
from generate_graph_neo4j import *
from derivation_afd_min import *
from derivation_afn import is_accepted
from derivation_afd import derivation_afd
from generate_txt import *

if __name__ == "__main__":
        try:
            infix = input("Ingresa la regexp en formato infix: ")

            infix_with_concatenations = add_implicit_concatenations(infix)
            print(infix_with_concatenations)
            result_postfix = sunting_yard(infix_with_concatenations)
            print(
                f"El resultado de la cadena {infix} en formato infix a postfix es: \n{''.join(result_postfix)}")

            # Ejemplo de uso thompson
            postfix_expression = result_postfix
            afn = build_afn_from_postfix(postfix_expression)


            result_afn = f'''--- AFN ---
            ESTADO INICIAL: {afn.initial_state}
            ESTADO FINAL: {afn.final_state}
            TRANSICIONES: {afn.transitions}
            '''
            generate_txt('AFN.txt', result_afn)
            
            AFD = subsets(afn)
            result_afd = f'''--- AFD ---
            ESTADOS: {AFD['STATES']}
            SÍMBOLOS: {AFD['SYMBOLS']}
            ESTADO INICIAL: {AFD['INITIAL_STATE']}
            ACEPTACION: {AFD['ACCEPTANCE']}
            TRANSICIONES: {AFD['TRANSITIONS']}
            '''
            generate_txt('AFD.txt', result_afd)



            AFD_MIN = hopcroft_minimization(AFD)

            result_afd_min = f'''--- AFD MINIMAL ---
            ESTADOS: {AFD_MIN['STATES']}
            SÍMBOLOS: {AFD_MIN['SYMBOLS']}
            ESTADO INICIAL: {AFD_MIN['INITIAL_STATE']}
            ACEPTACION: {AFD_MIN['ACCEPTANCE']}
            TRANSICIONES: {AFD_MIN['TRANSITIONS']}
            '''
            generate_txt('AFD_MIN.txt', result_afd_min)

            try:
                generate_graph_neo4j(AFD_MIN)
            except Exception as err:
                print("Para generar el gráfico, se debe de comprobar la conexión a Neo4J.")

            finish = False
            while not finish:
                r = input("¿Desea probar una cadena? (y/n):")

                if(r == "n"):
                    finish = True
                    continue
                elif r == 'y':
                    try:
                        word = input("Ingresar cadena de prueba: ").replace("ε","")
                        #verificar afn
                        is_accepted(afn, word)
                        derivation_afd(AFD, word)
                        derivation_afd_min(AFD_MIN, word)
                    except Exception as ex:
                        print(ex)

        except Exception as err:
            print("Ejecución finalizada con éxito :)")

