import random
# Importamos los datos y la visualizacion del pokedex
from pokedex import CATALOGO_POKEMON, mostrar_catalogo_disponible
from pokemon_clases import PokemonAgua, PokemonFuego, PokemonPlanta, PokemonElectrico

# Funcion seleccionar pokemon para que el jugador selecciones su combatiente
def seleccionar_pokemon(mensaje_instruccion):
    while True:
        # Llamo a la funcion que imprime la lista de Pokemons en pantalla
        mostrar_catalogo_disponible()
        # Para capturar los errores de entrada y evitar que el programa colapse
        try:
            # Captura la entrada del usuario del numero del pokemon
            opcion = input(mensaje_instruccion)
            # Validacion para ver si el numero ingresado existe en el catalogo
            if opcion not in CATALOGO_POKEMON:
                print("Error: El número seleccionado no está en el catálogo.")
                # Reinicia el bucle para pedir la opcion nuevamente
                continue
            
            datos = CATALOGO_POKEMON[opcion]
            tipo = datos["tipo"]
            nombre = datos["nombre"]
            puntos_salud_maximos = datos["hp_maximo"]
            puntos_energia_maximos = datos["energia_maxima"]
            
            print(f"¡Has seleccionado a {nombre}!")
            
            if tipo == "Fuego":
                return PokemonFuego(nombre, puntos_salud_maximos, puntos_energia_maximos)
            elif tipo == "Agua":
                return PokemonAgua(nombre, puntos_salud_maximos, puntos_energia_maximos)
            elif tipo == "Planta":
                return PokemonPlanta(nombre, puntos_salud_maximos, puntos_energia_maximos)
            elif tipo == "Electrico":
                return PokemonElectrico(nombre, puntos_salud_maximos, puntos_energia_maximos)
        except ValueError:
            print("Error: Ingrese un número válido.")      
        except Exception as error:
            print(f"Error en la selección: {error}")

def ejecutar_turno(jugador, oponente, controlador=False):
    print("\nTURNO DE: " + jugador.nombre) 
    print("[HP: " + str(jugador.hp_actual) + "/" + str(jugador.hp_maximo) + "] | [EP: " + str(jugador.energia_actual) + "/" + str(jugador.energia_maxima) + "]")

    # Determina si la acción la toma un jugador o la computadora (Modo PvE)
    if controlador:
        opcion_accion = random.randint(1, 3) 
        print(f"La computadora elige: {opcion_accion}")
    else:
        # Bucle de validación para el turno del jugador
        while True:
            try:
                print("¿Qué acción deseas realizar?")
                print("1. Atacar (Costo: 15 EP)\n2. Defender (Costo: 5 EP)\n3. Descansar (Restaura: 20 EP)")
                opcion_accion = int(input("> Opción: "))
                if opcion_accion in [1, 2, 3]:
                    break
                print("Opción no válida.")
            except ValueError:
                # Evita que el programa colapse si se ingresan letras o símbolos
                print("Error: Debe ingresar un número entero.")

    # Ejecutamos los métodos que definisnos en a clase base y la que fue sobrescrita en las hijas
    if opcion_accion == 1:
        mensaje_resultado, dano = jugador.atacar(oponente)
        print(mensaje_resultado)
    elif opcion_accion == 2:
        # Activa el estado de defensa para reducir el daño entrante
        print(jugador.defender())
    elif opcion_accion == 3:
        # Restaura puntos de energía (EP) sacrificando el turno
        print(jugador.descansar())
