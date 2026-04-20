from abc import ABC, abstractmethod

class Pokemon(ABC):
    def __init__(self, nombre, hp_maximo, energia_maxima):
        self.nombre = nombre
        self.hp_maximo = hp_maximo
        self. energia_maxima = energia_maxima
        self.__hp_actual = 100
        self.__energia_actual = 100
    
    @property
    def hp_actual(self):
        return self.__hp_actual
    
    # Setter para no permitir valor negativos en hp
    @hp_actual.setter
    def hp_actual(self, valor):
        if valor < 0:
            self.__hp_actual = 0
        else:
            self.__hp_actual = valor

    @property
    def energia_actual(self):
        return self.__energia_actual
    
    # Setter que no permite energia negativa ni maxima
    @energia_actual.setter
    def energia_actual(self, valor):
        if valor < 0:
            self.__energia_actual = 0
        else:
            self.__energia_actual = valor

    @abstractmethod
    def atacar(self):
        pass

    def defender(self):
        costo_ep = 5

        if self.energia_actual >= costo_ep:
            self.energia_actual -= costo_ep
        
    def descansar(self):
        restaurar_ep = 20
        self.energia_actual += restaurar_ep

class PokemonAgua(Pokemon):
    def atacar(self, oponente):
        pass

class PokemonFuego(Pokemon):
    def atacar(self, oponente):
        pass

class PokemonPlanta(Pokemon):
    def atacar(self, oponente):
        pass

class PokemonElectrico(Pokemon):
    def atacar(self, oponente):
        pass