from abc import ABC, abstractmethod

class Servicio(ABC):
    def __init__(self, nombre, costo_base):
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, cantidad, **kwargs):
        pass

class AsesoriaAcademica(Servicio):
    def calcular_costo(self, horas, es_grupal=False):
        # Polimorfismo: cálculo con parámetro opcional
        precio = self.costo_base * horas
        return precio * 1.20 if es_grupal else precio

class ReservaAuditorio(Servicio):
    def calcular_costo(self, horas, con_limpieza=True):
        # Polimorfismo: incluye un cargo fijo adicional
        cargo_extra = 15.0 if con_limpieza else 0.0
        return (self.costo_base * horas) + cargo_extra

class PrestamoEquipo(Servicio):
    def calcular_costo(self, dias):
        # Polimorfismo: descuento por volumen
        total = self.costo_base * dias
        if dias > 5:
            total *= 0.90  # 10% descuento
        return total