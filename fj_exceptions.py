#----------------------------------------------------
#--- ARCHIVO: fj_exceptions.py ---------------------
# Define todas las excepciones personalizadas para el 
# sistema de gestión de reservas.
#----------------------------------------------------


#=======================================
# --- EXCEPCION BASE -------------------
# todas las demas herendan de esta clase
#=======================================

class SistemaError(Exception):
    """Clase base para las excepciones del sistema."""
    pass


#============================================
# --- EXCEPCIONES DE CLIENTE ----------------
# Errores relacionados con datos del cliente.
#============================================

class ClienteError(SistemaError):
    """Errores relacionados con la gestión de clientes."""
    pass

class AutenticacionError(SistemaError):
    """Error en login o registro."""
    pass

class CampoVacioError(ClienteError):
    """Error cuando un campo del cliente está vacío."""
    pass

class CorreoInvalidoError(ClienteError):
    """Error cuando el correo del cliente no es válido."""
    pass

class NombreInvalidoError(ClienteError):
    """Error cuando el nombre del cliente no es válido."""
    pass

class PasswordInvalidoError(ClienteError):
    """Error cuando el password del cliente no es válido."""
    pass

#================================
# --- ERRORES DE LOG ------------
#================================

class LogError(Exception):
    """Errores relacionados con la gestión de logs."""
    pass


#=============================================
# --- EXCEPCIONES DE SERVICIOS ---------------
# Errores relacionados con datos de servicios.
#=============================================


class ReservaInvalidaError(SistemaError):
    """Error cuando los parámetros de reserva no cumplen las reglas."""
    pass

class ServicioNoDisponibleError(SistemaError):
    """Error si el servicio solicitado no existe o está inactivo."""
    pass