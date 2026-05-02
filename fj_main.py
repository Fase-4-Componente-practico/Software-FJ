import logging
from fj_models import Estudiante
from fj_services import AsesoriaAcademica, ReservaAuditorio, PrestamoEquipo
from fj_operations import Reserva
from fj_exceptions import UniversidadError, AutenticacionError

# Configuración del Log
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

    def menu_principal(self):
        while True:
            print("\n--- SOFTWARE FJ: GESTIÓN UNIVERSITARIA ---")
            print("1. Registro de Estudiante")
            print("2. Login")
            print("3. Salir")
            op = input("Seleccione: ")
            
            try:
                if op == "1": self.registrar()
                elif op == "2": self.login()
                elif op == "3": break
                else: print("Opción inválida.")
            except UniversidadError as e:
                print(f"\n[!] Error: {e}")
            except Exception as e:
                logging.critical(f"Error inesperado: {e}", exc_info=True)
                print("\n[X] Error crítico. Contacte a soporte.")

    def registrar(self):
        id_u = input("ID de Usuario: ")
        if id_u in self.usuarios: raise AutenticacionError("El usuario ya existe.")
        nom = input("Nombre completo: ")
        pwd = input("Contraseña: ")
        self.usuarios[id_u] = Estudiante(nom, id_u, pwd)
        logging.info(f"Nuevo usuario registrado: {id_u}")
        print("Registro exitoso.")

    def login(self):
        id_u = input("ID: ")
        pwd = input("Password: ")
        user = self.usuarios.get(id_u)
        
        if user and user.verificar_password(pwd):
            logging.info(f"Login exitoso: {id_u}")
            self.area_usuario(user)
        else:
            raise AutenticacionError("ID o contraseña incorrectos.")

    def area_usuario(self, user):
        while True:
            print(f"\n--- BIENVENIDO, {user.nombre} ---")
            print("1. Nueva Reserva / Servicio")
            print("2. Ver mis actividades")
            print("3. Cerrar Sesión")
            op = input("Seleccione: ")

            if op == "1":
                print("\nServicios disponibles:")
                for k, v in self.servicios.items(): print(f"{k}. {v.nombre}")
                s_op = input("Seleccione servicio: ")
                
                try:
                    if s_op not in self.servicios: raise UniversidadError("Servicio no válido.")
                    dur = int(input("Ingrese cantidad (Horas/Días): "))
                    res = Reserva(user, self.servicios[s_op], dur)
                    ticket = res.procesar()
                    user.historial_reservas.append(ticket)
                    print(f"\nEXITO: {ticket}")
                except ValueError:
                    print("Error: La duración debe ser un número entero.")
                except UniversidadError as e:
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

