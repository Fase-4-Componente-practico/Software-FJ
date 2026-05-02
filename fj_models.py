from abc import ABC, abstractmethod

class EntidadSistema(ABC):
    @abstractmethod
    def obtener_detalles(self):
        pass

class Estudiante(EntidadSistema):
    def __init__(self, nombre, id_usuario, password):
        self._nombre = nombre             # Protegido
        self.__id_usuario = id_usuario    # Privado
        self.__password = password        # Privado
        self.historial_reservas = []

    @property
    def nombre(self):
        return self._nombre

    @property
    def id_usuario(self):
        return self.__id_usuario

    def verificar_password(self, password):
        return self.__password == password

    def obtener_detalles(self):
        return f"Estudiante: {self._nombre} | ID: {self.__id_usuario}"