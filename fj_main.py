import logging
from fj_models import Cliente
from fj_services import AsesoriaAcademica, ReservaAuditorio, PrestamoEquipo
from fj_operations import Reserva
from fj_exceptions import SistemaError,AutenticacionError,CampoVacioError,CorreoInvalidoError,logError


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
            print("\n--- SOFTWARE FJ: GESTIÓN CLIENTES---")
            print("1. Registro de Cliente")
            print("2. Login")
            print("3. Salir")
            op = input("Seleccione: ")
            
            try:
                if op == "1": self.registrar()
                elif op == "2": self.login()
                elif op == "3": break
                else: print("Opción inválida.")
                
            except SistemaError as e:
                print(f"\n[!] Error: {e}")
                
            except Exception as e:
                logging.critical(f"Error inesperado: {e}", exc_info=True)
                print("\n[X] Error crítico. Contacte a soporte.")


    def registrar(self):
        try:
            id_u = input("Usuario: ").strip()
            nom = input("Nombre completo: ").strip()
            mail = input("Correo electrónico: ").strip()
            pwd = input("Contraseña: ").strip()
            
            if id_u in self.usuarios:
                raise SistemaError("El usuario ya existe")
            
            cliente = Cliente(id_u, nom, mail, pwd)
            self.usuarios[id_u] = cliente
            logging.info(f"Nuevo usuario registrado: {id_u}")
            print("Registro exitoso.")
            
        except (CampoVacioError, CorreoInvalidoError,SistemaError,) as e:
            print(f"Error: {e}")
    
        except logError as e:
            print(f"Error al registrar el usuario: {e}")
            
            
    def login(self):
        id_u = input("Usuario: ")
        pwd = input("Contraseña: ")
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

