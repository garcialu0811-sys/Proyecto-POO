from abc import ABC, abstractmethod
import random

class Pokemon(ABC):
    def __init__(self, nombre, hp_maximo, energia_maxima):
        self.nombre = nombre
        self.hp_maximo = hp_maximo
        self. energia_maxima = energia_maxima
        self.__hp_actual = 100
        self.__energia_actual = 100
        self.__defendiendo = False

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

    @property
    def defendiendo(self):
        return self.__defendiendo
    
    @defendiendo.setter
    def defendiendo(self, nuevo_valor):
        self.__defendiendo = nuevo_valor

    @abstractmethod
    def atacar(self):
        pass

    def defender(self):
        costo_ep = 5

        if self.energia_actual >= costo_ep:
            self.energia_actual -= costo_ep
            self.__defendiendo = True
            return f"{self.nombre} se ha puesto en fuardia. Reducirá el daño del próximo ataque a la mitad."
        else:
            return f"{self.nombre} no tiene sificiente enerfia para defenderse (Necesita {costo_ep} EP)."
        
    # Método descansar
    def descansar(self):
        restaurar_ep = 20
        self.energia_actual += restaurar_ep
        #Cancelamos el estado de defensa al descansar
        self.defendiendo = False
        return f"{self.nombre} descansa y recupera {restaurar_ep} EP. Ahora tiene {self.energia_actual}/{self.energia_maxima} EP."
    
    # Metodo recibir daño
    def recibir_dano(self, dano):
        dano_final = dano  # Guarda daño inicial
        
        if self.defendiendo:  # Si estaba defendiendo
            dano_final = dano // 2  # Reduce daño a la mitad
            self.defendiendo = False  # Desactiva defensa
        
        self.hp_actual -= dano_final  # Resta vida
        return dano_final  # Retorna daño aplicado
    
    # Verifica si sigue vivo
    def esta_vivo(self):
        return self.hp_actual > 0
    
    # Muestra información del objeto en formato legible
    def __str__(self): 
        return f"{self.nombre} [{self.tipo}] HP:{self.hp_actual}/{self.hp_maximo} EP:{self.energia_actual}/{self.energia_maxima}"
    
    # Será sobrescrito por cada clase hija para definir su tipo específico
    @property
    def tipo(self):
        return "Desconocido"
    

class PokemonAgua(Pokemon):
    @property
    def tipo(self):
        return "Agua"

    def atacar(self, oponente):
        costo_ep = 15  # Energía necesaria

        if self.energia_actual < costo_ep:
            return f"{self.nombre} no tiene suficiente energía para atacar (Necesita {costo_ep} EP).", 0

        self.energia_actual -= costo_ep  # Consume energía
        dano_base = 20  # Daño base
        
        multiplicador = 1  # Multiplicador normal
        mensaje_efectividad = ""  # Texto vacío
        
        if oponente.tipo == "Fuego":  # Ventaja
            multiplicador = 2
            mensaje_efectividad = "¡Es súper efectivo!"
        elif oponente.tipo == "Planta":  # Desventaja
            multiplicador = 0.5
            mensaje_efectividad = "No es muy efectivo..."
        
        dano_total = int(dano_base * multiplicador)  # Calcula daño total
        dano_real = oponente.recibir_dano(dano_total)  # Aplica daño
        
        mensaje = f"{self.nombre} usa un ataque de AGUA! {mensaje_efectividad} {oponente.nombre} recibe {dano_real} puntos de daño."
        return mensaje, dano_real


class PokemonFuego(Pokemon):
    def atacar(self, oponente):
        pass

class PokemonPlanta(Pokemon):
    def atacar(self, oponente):
        pass

class PokemonElectrico(Pokemon):
    def atacar(self, oponente):
        pass