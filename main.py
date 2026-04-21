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