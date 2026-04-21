from abc import ABC, abstractmethod
import random

class Pokemon(ABC):
    def __init__(self, nombre, hp_maximo, energia_maxima):
        self.nombre = nombre
        self.hp_maximo = hp_maximo
        self. energia_maxima = energia_maxima
        self.__hp_actual = hp_maximo
        self.__energia_actual = energia_maxima
        self.__defendiendo = False
        self.__paralizado = False
        
    # Getter de hp_actual
    @property
    def hp_actual(self):
        return self.__hp_actual
    
    # Setter para no permitir valor negativos en hp
    @hp_actual.setter
    def hp_actual(self, nuevo_valor):
        # Si es menor a 0 lo deja en 0
        if nuevo_valor < 0:
            self.__hp_actual = 0
        # Si no, guarda el valor normal
        else:
            self.__hp_actual = nuevo_valor
            
    # Getter de energia_actual
    @property
    def energia_actual(self):
        return self.__energia_actual
    
    # Setter que no permite energia negativa ni mayor al maximo
    @energia_actual.setter
    def energia_actual(self, nuevo_valor):
        # Si es negativa la deja en 0
        if nuevo_valor < 0:
            self.__energia_actual = 0
        # Si supera el maximo, la iguala al maximo
        elif nuevo_valor > self.energia_maxima:
            self.__energia_actual = self.energia_maxima
        else:
            self.__energia_actual = nuevo_valor

    @property
    def defendiendo(self):
        return self.__defendiendo
    
    @defendiendo.setter
    def defendiendo(self, nuevo_valor):
        self.__defendiendo = nuevo_valor
        
    @property
    def paralizado(self):
        return self.__paralizado

    @paralizado.setter
    def paralizado(self, nuevo_valor):
        self.__paralizado = nuevo_valor
    
    # Metodo abstracto que sera sobrescrito por cada clase hija
    @abstractmethod
    def atacar(self, oponente):
        pass
    
    # Metodo defender, que consume 5 EP y reduce el da;o al proximo ataque a la mitad
    def defender(self):
        costo_ep = 5

        if self.energia_actual >= costo_ep:
            self.energia_actual -= costo_ep
            self.defendiendo = True
            return f"{self.nombre} se ha puesto en guardia. Reducirá el daño del próximo ataque a la mitad."
        else:
            return f"{self.nombre} no tiene sificiente energía para defenderse (Necesita {costo_ep} EP)."
        
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
        return dano_final  # Retorna daño recibido
    
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
        if self.paralizado:
            self.paralizado = False
            return f"{self.nombre} está paralizado y no puede moverse. Pierde su turno.", 0
        
        costo_ep = 15  # Energía necesaria

        if self.energia_actual < costo_ep:
            return f"{self.nombre} no tiene suficiente energía para atacar (Necesita {costo_ep} EP).", 0

        self.energia_actual -= costo_ep  # Consume energía
        dano_base = 20  # Daño base
        multiplicador = 1  # Multiplicador normal
        mensaje_efectividad = ""  # Texto de efectividad
        
        if isinstance(oponente, PokemonFuego):
            multiplicador = 2
            mensaje = "¡Es súper efectivo!"
        elif isinstance(oponente, PokemonPlanta):
            multiplicador = 0.5
            mensaje = "El ataque no fue muy efectivo..."
        
        dano_total = int(dano_base * multiplicador)  # Calcula daño total
        dano_real = oponente.recibir_dano(dano_total)  # Aplica daño
        
        mensaje = f"{self.nombre} usa un ataque de AGUA! {mensaje_efectividad} {oponente.nombre} recibe {dano_real} puntos de daño."
        return mensaje, dano_real


class PokemonFuego(Pokemon):
    @property
    def tipo(self):
        return "Fuego"

    def atacar(self, oponente):
        if self.paralizado:
            self.paralizado = False
            return f"{self.nombre} está paralizado y no puede moverse. Pierde su turno.", 0
        
        costo_ep = 15

        if self.energia_actual < costo_ep:
            return f"{self.nombre} no tiene suficiente energía para atacar (Necesita {costo_ep} EP).", 0

        self.energia_actual -= costo_ep
        dano_base = 20
        multiplicador = 1
        mensaje_efectividad = ""
        
        if isinstance(oponente, PokemonPlanta):
            multiplicador = 2
            mensaje_efectividad = "¡Es súper efectivo!"

        elif isinstance(oponente, PokemonAgua):
            multiplicador = 0.5
            mensaje_efectividad = "El ataque no fue muy efectivo..."

        dano_total = int(dano_base * multiplicador)
        dano_real = oponente.recibir_dano(dano_total)

        texto = f"{self.nombre} usa ataque de FUEGO. {mensaje_efectividad} {oponente.nombre} recibe {dano_real} puntos de daño."
        return texto, dano_real

class PokemonPlanta(Pokemon):
    @property
    def tipo(self):
        return "Planta"

    def atacar(self, oponente):
        if self.paralizado:
            self.paralizado = False
            return f"{self.nombre} está paralizado y no puede moverse. Pierde su turno.", 0
        
        costo_ep = 15

        if self.energia_actual < costo_ep:
            return f"{self.nombre} no tiene suficiente energía para atacar (Necesita {costo_ep} EP).", 0

        self.energia_actual -= costo_ep
        dano_base = 20
        multiplicador = 1
        mensaje_efectividad = ""
        
        if isinstance(oponente, PokemonAgua):
            multiplicador = 2
            mensaje_efectividad = "¡Es súper efectivo!"

        elif isinstance(oponente, PokemonFuego):
            multiplicador = 0.5
            mensaje_efectividad = "El ataque no fue muy efectivo..."

        dano_total = int(dano_base * multiplicador)
        dano_real = oponente.recibir_dano(dano_total)

        texto = f"{self.nombre} usa ataque de PLANTA. {mensaje_efectividad} {oponente.nombre} recibe {dano_real} puntos de daño."
        return texto, dano_real

class PokemonElectrico(Pokemon):
    @property
    def tipo(self):
        return "Electrico"

    def atacar(self, oponente):
        if self.paralizado:
            self.paralizado = False
            return f"{self.nombre} está paralizado y no puede moverse. Pierde su turno.", 0
        
        costo_ep = 15

        if self.energia_actual < costo_ep:
            return f"{self.nombre} no tiene suficiente energía para atacar (Necesita {costo_ep} EP).", 0

        self.energia_actual -= costo_ep
        dano_base = 20
        mensaje_efectividad = ""
        
        if random.random() < 0.2: # 20% de probabilidad
            oponente.paralizado = True
            mensaje_efectividad = f"¡{oponente.nombre} ha quedado paralizado y perderá su próximo turno!"
            
        dano_real = oponente.recibir_dano(dano_base)

        texto = f"{self.nombre} usa ataque ELÉCTRICO. {mensaje_efectividad} {oponente.nombre} recibe {dano_real} puntos de daño."
        return texto, dano_real