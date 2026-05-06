#--------------------------------
# --- EXCEPCIONES DEL SISTEMA ---
#--------------------------------


class SistemaError(Exception):
    """Clase base para las excepciones del sistema."""
    pass


#================================
# --- EXCEPCIONES DE CLIENTE ----
#================================

class clienteError(SistemaError):
    """Errores relacionados con la gestión de clientes."""
    pass

class AutenticacionError(SistemaError):
    """Error en login o registro."""
    pass

class CampoVacioError(clienteError):
    """Error cuando un campo del cliente está vacío."""
    pass

class CorreoInvalidoError(clienteError):
    """Error cuando el correo del cliente no es válido."""
    pass


#================================
# --- ERRORES DE LOG ------------
#================================

class logError(Exception):
    """Errores relacionados con la gestión de logs."""
    pass


#================================
# --- EXCEPCIONES DE SERVICIOS ----
#================================


class ReservaInvalidaError(SistemaError):
    """Error cuando los parámetros de reserva no cumplen las reglas."""
    pass

class ServicioNoDisponibleError(SistemaError):
    """Error si el servicio solicitado no existe o está inactivo."""
    pass