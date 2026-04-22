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
        
# Funcion principal 
def iniciar_simulador():
    # Encabezado visual del programa
    print("="*40)
    print(f'{" SIMULADOR DE BATALLAS POKÉMON (POO) ":^40}')
    print("="*40)

    # Selección del modo de juego inicial
    modo_de_juego = ""
    while modo_de_juego != "1" and modo_de_juego != "2":
        print("Seleccione el Modo de Juego:")
        print("1. Jugador vs Jugador")
        print("2. Jugador vs Computadora")
        modo_de_juego = input("> Opción: ")

    # Configuración del primer combatiente
    luchador_uno = seleccionar_pokemon("Jugador 1, elija el número de su Pokémon: ")
    
    # Configuración del segundo combatiente según el modo seleccionado
    if modo_de_juego == "2":
        print("\nComputadora eligiendo combatiente...")
        
        # Convertimos el diccionario a lista para obtener los IDs al azar
        identificadores_disponibles = list(CATALOGO_POKEMON)
        id_elegido_computadora = random.choice(identificadores_disponibles)
        
        # Extraemos los datos del rival elegido al azar
        datos_rival = CATALOGO_POKEMON[id_elegido_computadora]
        tipo_rival = datos_rival["tipo"]
        nombre_rival = datos_rival["nombre"]
        vida_rival = datos_rival["hp_maximo"]
        energia_rival = datos_rival["energia_maxima"]

        # Instanciación según el tipo para la computadora
        if tipo_rival == "Fuego":
            luchador_dos = PokemonFuego(nombre_rival, vida_rival, energia_rival)
        elif tipo_rival == "Agua":
            luchador_dos = PokemonAgua(nombre_rival, vida_rival, energia_rival)
        elif tipo_rival == "Planta":
            luchador_dos = PokemonPlanta(nombre_rival, vida_rival, energia_rival)
        else:
            luchador_dos = PokemonElectrico(nombre_rival, vida_rival, energia_rival)
        
        print("¡La computadora ha seleccionado a " + luchador_dos.nombre + "!")
    else:
        luchador_dos = seleccionar_pokemon("Jugador 2, elija el número de su Pokémon: ")

    print("\n¡COMIENZA LA BATALLA!")
    print(luchador_uno.nombre + " (" + luchador_uno.tipo + ") vs " + luchador_dos.nombre + " (" + luchador_dos.tipo + ")")

    # Ciclo principal de combate por turnos
    turno_del_primero = True
    
    # El combate sigue mientras ambos esten vivos segun su HP
    while luchador_uno.esta_vivo() and luchador_dos.esta_vivo():
        if turno_del_primero:
            ejecutar_turno(luchador_uno, luchador_dos)
        else:
            # Si es modo 2, el segundo turno es controlado por el sistema automatico
            es_computadora = False
            if modo_de_juego == "2":
                es_computadora = True
            
            ejecutar_turno(luchador_dos, luchador_uno, es_computadora)
        
        # Alterna el turno entre los combatientes
        turno_del_primero = not turno_del_primero

    # Declaración del ganador una vez que alguien se queda sin vida
    print("\n" + "*"*30)
    if luchador_uno.esta_vivo():
        print("\n¡EL GANADOR ES " + luchador_uno.nombre + "!")
    else:
        print("n¡EL GANADOR ES " + luchador_dos.nombre + "!")
    print("*"*30)

# Punto de entrada principal para ejecutar el script
if __name__ == "__main__":
    iniciar_simulador()
