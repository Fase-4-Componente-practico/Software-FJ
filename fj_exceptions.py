
# --- EXCEPCIONES PERSONALIZADAS ---


class UniversidadError(Exception):
    """Clase base para todas las excepciones del sistema."""
    pass

class AutenticacionError(UniversidadError):
    """Error en login o registro."""
    pass

class ReservaInvalidaError(UniversidadError):
    """Error cuando los parámetros de reserva no cumplen las reglas."""
    pass

class ServicioNoDisponibleError(UniversidadError):
    """Error si el servicio solicitado no existe o está inactivo."""
    pass