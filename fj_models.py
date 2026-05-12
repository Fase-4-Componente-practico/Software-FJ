from fj_exceptions import (CampoVacioError, CorreoInvalidoError, LogError, NombreInvalidoError, PasswordInvalidoError)

# =========================================
# ---- REGISTRO DE LOGS -------------------
# =========================================

def registrar_log(mensaje):
    try:
        with open("logs.txt", "a") as archivo:
            archivo.write(mensaje + "\n")
    except Exception as e:
       raise LogError("Error al escribir en log:", e)

# =========================================
# CLIENTE - Implementado por Gerardo
# =========================================

class Cliente:
    def __init__(self, usuario, nombre, correo, password):
        try:
            if not usuario or usuario.strip() == "":
                raise CampoVacioError("Usuario vacío")
                       
            if not nombre or nombre.strip() == "":
                raise CampoVacioError("Nombre vacío")
            
            if not nombre.replace(" ", "").isalpha():
                raise NombreInvalidoError("Nombre inválido. Solo se permiten letras y espacios.")

            if "@" not in correo or "." not in correo:
                raise CorreoInvalidoError("Correo inválido")
            
            if not password or password.strip() == "":
                raise CampoVacioError("Contraseña vacía. Ingrese una contraseña")
            
            if len(password) < 8:
                raise PasswordInvalidoError("Contraseña inválida. Debe tener al menos 8 caracteres.")
            
            self.__usuario = usuario
            self.__nombre = nombre
            self.__correo = correo
            self.__password = password
            
            self.historial_reservas = []
           
        except (CampoVacioError, CorreoInvalidoError, NombreInvalidoError, PasswordInvalidoError) as e:
            registrar_log(f"Error cliente: {e}")
            raise

    def get_usuario(self):
        return self.__usuario
    
    def get_nombre(self):
        return self.__nombre

    def get_correo(self):
        return self.__correo
    
    
    def verificar_password(self, pwd):
        return self.__password == pwd


    def set_correo(self, nuevo_correo):
        try:
            if "@" not in nuevo_correo or "." not in nuevo_correo:
                raise CorreoInvalidoError("Correo inválido")

            self.__correo = nuevo_correo

        except CorreoInvalidoError as e:
            registrar_log(f"Error al actualizar correo: {e}")
            raise
        
        
    def __str__(self):
        return f"Cliente: {self.__nombre} - {self.__correo}"    
        
    def to_dict(self):
        return {
            "nombre": self.__nombre,
            "correo": self.__correo
        } 
    def es_valido(self):
        return bool(self.__nombre and "@" in self.__correo and "." in self.__correo)
