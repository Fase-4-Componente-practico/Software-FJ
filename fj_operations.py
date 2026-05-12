import logging
from datetime import datetime
from fj_exceptions import ReservaInvalidaError

class Reserva:
    def __init__(self, cliente, servicio, duracion, **kwargs):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.kwargs = kwargs
        self.fecha = datetime.now()

    def procesar(self):
        try:
            if not isinstance(self.duracion, int) or self.duracion <= 0:
                raise ReservaInvalidaError(f"Duración inválida: {self.duracion}")
            
            resultado_calculo = self.servicio.calcular_costo(self.duracion, **self.kwargs)
            costo = resultado_calculo["costo"]
            detalle = resultado_calculo["detalle"]
            
            resultado = (f"Fecha y hora actual: {self.fecha.strftime('%Y-%m-%d %H:%M')} | "
                         f"\nServicio: {self.servicio.nombre} | "
                         f"\nCosto: ${costo:,.0f} | "
                         f"\nDetalle: {detalle}")
            return resultado
            
        except Exception as e:
            # Encadenamiento de excepciones y log
            logging.error(f"Error procesando reserva para {self.cliente.get_nombre()}: {e}")
            raise ReservaInvalidaError("No se pudo completar la reserva por datos inconsistentes.") from e

def registrar_reserva(lista_reservas, cliente, servicio, duracion,**kwargs):
    try:
        reserva = Reserva(cliente, servicio, duracion, **kwargs)
        resultado = reserva.procesar()
        lista_reservas.append(reserva)

        logging.info(f"Reserva registrada para {cliente.get_nombre()}")
        return resultado

    except ReservaInvalidaError as e:
        logging.error(f"Error al registrar reserva: {e}")
        return None

def mostrar_reservas(lista_reservas):
    try:
        if len(lista_reservas) == 0:
            logging.info("No hay reservas registradas")
            return

        for reserva in lista_reservas:
            print(reserva.procesar())

    except Exception as e:
        logging.error(f"Error al mostrar reservas: {e}")

def cancelar_reserva(lista_reservas, indice):
    try:
        if indice < 0 or indice >= len(lista_reservas):
            raise ReservaInvalidaError("Reserva no encontrada")

        reserva_cancelada = lista_reservas.pop(indice)

        logging.info(f"Reserva cancelada: {reserva_cancelada.servicio.nombre}")
        return "Reserva cancelada correctamente"

    except ReservaInvalidaError as e:
        logging.error(f"Error al cancelar reserva: {e}")
        return None
  
