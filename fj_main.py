import logging
from fj_models import Cliente
from fj_services import AsesoriaAcademica, ReservaAuditorio, PrestamoEquipo
from fj_operations import Reserva
from fj_exceptions import SistemaError,AutenticacionError,CampoVacioError,CorreoInvalidoError,NombreInvalidoError,PasswordInvalidoError,LogError


logging.basicConfig(
    filename='software_fj_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class App:
    def __init__(self):
        self.usuarios = {}
        self.servicios = {
            "1": AsesoriaAcademica("Asesoría Académica", 20.0),
            "2": ReservaAuditorio("Auditorio Principal", 100.0),
            "3": PrestamoEquipo("Laptop Pro", 15.0)
        }
    
    #====================================
    # fUNCIONES PARA VALIDACIÓN DE DATOS 
    #====================================
    
    def pedir_datos(self, mensaje, tipo="texto"):
        while True:
            dato = input(mensaje).strip()
            
            if not dato:
                print("Error: El campo no puede estar vacío. Intente nuevamente.")
                continue
            
            if tipo == "nombre":
                if not self.validar_nombre(dato):
                    print("Error: El nombre debe contener solo letras y espacios. Intente nuevamente.")
                    continue
            
            elif tipo == "correo":
                if not self.validar_correo(dato):
                    print("Error: El correo debe contener '@' y '.'. Intente nuevamente.")
                    continue
                
            elif tipo == "password":
                if not self.validar_password(dato):
                    print("Error: El password debe tener al menos 8 caracteres. Intente nuevamente.")
                    continue
                
            return dato
        
    
    def validar_nombre(self, nombre):
        return nombre.replace(" ", "").isalpha()
    
    
    def validar_correo(self, correo):
        
        return "@" in correo and "." in correo
    
    def validar_password(self, password):
        return len(password) >= 8       
    
        
    #====================================
    # MENU PRINCIPAL DEL SISTEMA 
    #====================================
             

    def menu_principal(self):
        
        opciones = {
            "1": self.registrar,
            "2": self.login
        }
        while True:
            print("\n--- SOFTWARE FJ: GESTIÓN CLIENTES---")
            print("1. Registro de Cliente")
            print("2. Login")
            print("3. Salir")
            
            
            op = input("Seleccione: ")
            
            try:
                if op == "3": 
                    print("Saliendo del sistema. ¡Hasta luego!")
                    break
                
                elif op in opciones:
                    opciones[op]()
                    
                else:
                    print("Opción inválida. Por favor, seleccione una opción válida.")
                
                            
            except SistemaError as e:
                print(f"\n[!] Error: {e}")
                
            except Exception as e:
                logging.critical(f"Error inesperado: {e}", exc_info=True)
                print("\n[X] Error crítico. Contacte a soporte.")



    #====================================
    # REGISTRAR Y AUTENTICAR USUARIOS
    #====================================
    
    def registrar(self):
                
        try:
            id_u = self.pedir_datos("Usuario: ")
            nom = self.pedir_datos("Nombre completo: ", "nombre")
            mail = self.pedir_datos("Correo electrónico: ", "correo")
            pwd = self.pedir_datos("Password: ", "password")
            
             
            if id_u in self.usuarios:
                raise SistemaError("El usuario ya existe")
            
            
            cliente = Cliente(id_u, nom, mail, pwd)
            self.usuarios[id_u] = cliente           
            
            logging.info(f"Nuevo usuario registrado: {id_u}")
            print("Registro exitoso.")
                           
        except (CampoVacioError, CorreoInvalidoError, NombreInvalidoError, PasswordInvalidoError, SistemaError,) as e:
                print(f"Error: {e}")
        
        except LogError as e:
                print(f"Error al registrar el usuario: {e}")
            
    
    # =====================================
    # LOGIN Y ÁREA DE USUARIOS
    # =====================================      
    def login(self):
        id_u = input("Usuario: ")
        pwd = input("Password: ")
        user = self.usuarios.get(id_u)
        
        if user and user.verificar_password(pwd):
            logging.info(f"Login exitoso: {id_u}")
            self.area_usuario(user)
        else:
            raise AutenticacionError("ID o contraseña incorrectos.")

    def area_usuario(self, user):
        while True:
            print(f"\n--- BIENVENIDO, {user.get_nombre()} ---")
            print("1. Nueva Reserva / Servicio")
            print("2. Ver mis actividades")
            print("3. Cerrar Sesión")
            op = input("Seleccione: ")

            if op == "1":
                print("\nServicios disponibles:")
                for k, v in self.servicios.items(): print(f"{k}. {v.nombre}")
                s_op = input("Seleccione servicio: ")
                
                try:
                    if s_op not in self.servicios: raise SistemaError("Servicio no válido.")
                    dur = int(input("Ingrese cantidad (Horas/Días): "))
                    res = Reserva(user, self.servicios[s_op], dur)
                    ticket = res.procesar()
                    user.historial_reservas.append(ticket)
                    print(f"\nEXITO: {ticket}")
                except ValueError:
                    print("Error: La duración debe ser un número entero.")
                except SistemaError as e:
                    print(f"Error en reserva: {e}")

            elif op == "2":
                print("\n--- TUS ACTIVIDADES ---")
                for item in user.historial_reservas: print(item)
                if not user.historial_reservas: print("No hay registros.")

            elif op == "3":
                break

if __name__ == "__main__":
    app = App()
    app.menu_principal()

