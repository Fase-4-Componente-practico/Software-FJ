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
# =========================================
# CLIENTE - Implementado por Gerardo
# =========================================

class ClienteError(Exception):
    pass


def registrar_log(mensaje):
    try:
        with open("logs.txt", "a") as archivo:
            archivo.write(mensaje + "\n")
    except Exception as e:
        print("Error al escribir en log:", e)


class Cliente:
    def __init__(self, nombre, correo):
        try:
            if not nombre or nombre.strip() == "":
                raise ClienteError("Nombre vacío")

            if "@" not in correo or "." not in correo:
                raise ClienteError("Correo inválido")

            self.__nombre = nombre
            self.__correo = correo

        except ClienteError as e:
            registrar_log(f"Error cliente: {e}")
            raise

    def get_nombre(self):
        return self.__nombre

    def get_correo(self):
        return self.__correo

    def __str__(self):
        return f"Cliente: {self.__nombre} - {self.__correo}"
    def set_correo(self, nuevo_correo):
        try:
            if "@" not in nuevo_correo or "." not in nuevo_correo:
                raise ClienteError("Correo inválido")

            self.__correo = nuevo_correo

        except ClienteError as e:
            registrar_log(f"Error al actualizar correo: {e}")
            raise
    def to_dict(self):
        return {
            "nombre": self.__nombre,
            "correo": self.__correo
        }
