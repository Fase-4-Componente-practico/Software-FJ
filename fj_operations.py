import logging
from datetime import datetime
from fj_exceptions import ReservaInvalidaError

class Reserva:
    def __init__(self, estudiante, servicio, duracion):
        self.estudiante = estudiante
        self.servicio = servicio
        self.duracion = duracion
        self.fecha = datetime.now()

    def procesar(self):
        try:
            if not isinstance(self.duracion, int) or self.duracion <= 0:
                raise ReservaInvalidaError(f"Duración inválida: {self.duracion}")
            
            costo = self.servicio.calcular_costo(self.duracion)
            resultado = (f"ID: {self.fecha.strftime('%Y%m%d%H%M')} | "
                         f"Servicio: {self.servicio.nombre} | "
                         f"Costo: ${costo:.2f}")
            return resultado
        
        except Exception as e:
            # Encadenamiento de excepciones y log
            logging.error(f"Error procesando reserva para {self.estudiante.id_usuario}: {e}")
            raise ReservaInvalidaError("No se pudo completar la reserva por datos inconsistentes.") from e