import logging
from fj_models import Cliente
from fj_services import AsesoriaAcademica, ReservaAuditorio, PrestamoEquipo
from fj_operations import Reserva
from fj_exceptions import (SistemaError,AutenticacionError,CampoVacioError,CorreoInvalidoError,
                           NombreInvalidoError,PasswordInvalidoError,LogError)


logging.basicConfig(
    filename='software_fj_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class App:
    def __init__(self):
        self.usuarios = {}
        self.servicios = {
            "1": AsesoriaAcademica("Asesoría Académica", 5000.0),
            "2": ReservaAuditorio("Auditorio Principal", 10000.0),
            "3": PrestamoEquipo("Laptop Pro", 15000.0)
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
            "2": self.login,
            "3": self.simulacion_automatica
        }
        while True:
            print("\n--- SOFTWARE FJ GESTIÓN CLIENTES---\n")
            print("1. Registro de Cliente")
            print("2. Login")
            print("3. Simulación automática")
            print("4. Salir")

            op = input("Seleccione: ")
            
            try:
                if op == "4": 
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
                           
        except (CampoVacioError, CorreoInvalidoError, NombreInvalidoError,
                PasswordInvalidoError, SistemaError,) as e:
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
            print(f"\n--- BIENVENIDO {user.get_nombre()} ---\n")
            print("1. Nueva Reserva / Servicio")
            print("2. Ver mis actividades")
            print("3. Actualizar correo")
            print("4. Cancelar reserva")
            print("5. Información de usuario")
            print("6. Cerrar Sesión")
            op = input("Seleccione: ")

            if op == "1":
                print("\nServicios disponibles:")
                for k, v in self.servicios.items():
                    print(f"{k}. {v.nombre}")
                    print(f"Descripción: {v.describir_servicio()}")
                
                s_op = input("Seleccione servicio: ")
                
                try:
                    if s_op not in self.servicios: 
                        raise SistemaError("Servicio no válido.")
                    servicio = self.servicios[s_op]
                    dur = int(input("Ingrese cantidad (Horas): "))
                    
                    kwargs = {}
                    if s_op == "1":  # Asesoría académica
                        resp = input("¿Es asesoria grupal? (s/n): ").strip().lower()
                        kwargs["es_grupal"] = resp == "s"
                        
                    elif s_op == "2":  # Reserva de auditorio
                        resp = input("¿Incluir servicio de limpieza? (s/n): ").strip().lower()
                        kwargs["incluir_limpieza"] = resp == "s"
                        
                     
                    res = Reserva(user, servicio, dur, **kwargs)
                    ticket = res.procesar()
                    
                    user.historial_reservas.append(res)
                    print(f"\nEXITO: {ticket}")
                    
                except ValueError:
                    print("Error: La duración debe ser un número entero.")
                except SistemaError as e:
                    print(f"Error en reserva: {e}")

            elif op == "2":
                print("\n--- TUS ACTIVIDADES ---")
                if not user.historial_reservas:
                    print("No tienes actividades registradas.")
                else:
                    for i, item in enumerate(user.historial_reservas):
                        print(f"{i + 1}. {item.procesar()}")
                
                
            elif op == "3":
                print("\n--- ACTUALIZAR CORREO ---")
                nuevo_correo = self.pedir_datos("Nuevo correo: ","correo")
                try:
                    user.set_correo(nuevo_correo)
                    logging.info(f"Correo actualizado para: {user.get_usuario()}")
                    print("Correo actualizado exitosamente.")
                except CorreoInvalidoError as e:
                    print(f"Error al actualizar correo: {e}")
                    
            elif op == "4":
                print("\n--- CANCELAR RESERVA ---")
                if not user.historial_reservas:
                    print("No tienes reservas para cancelar.")
                else:
                    print("TUS RESERVAS:")
                    for i, item in enumerate(user.historial_reservas):
                        print(f"{i + 1}. {item.procesar()}")
                        
                    try:
                        num = int(input("Seleccione reserva a cancelar: "))
                        indice = num - 1
                        
                        if indice < 0 or indice >= len(user.historial_reservas):
                            raise SistemaError("Selección inválida.")
                        else:
                            reserva_cancelada = user.historial_reservas.pop(indice)
                            logging.info(f"Reserva cancelada por {reserva_cancelada.servicio.nombre}"
                                         f"por {user.get_usuario()}")
                            print("Reserva cancelada exitosamente.")
                    
                    except ValueError:
                        print("Error: Selección un item válido.")
            
            elif op == "5":
                print("\n--- Información de usuario ---")
                print(f"Usuario: {user.get_usuario()}")
                print(f"Nombre: {user.get_nombre()}")
                print(f"Correo: {user.get_correo()}")
                print(f"Reservas: {len(user.historial_reservas)} activas")
                
            elif op == "6":
                print("\nVolviendo al menú principal...")
                break
            
            
    # =====================================
    # SIMULACIÓN AUTOMÁTICA. 
    # PRUEBAS DE FUNCIONALIDAD Y VALIDACIONES
    # =====================================    
                
    def simulacion_automatica(self):       
        print("\n--- SIMULACIÓN AUTOMÁTICA ---")
        try:
            # Listas
            clientes = []
            reservas = []

            # 1. Cliente válido
            print("\n1. Creando cliente válido...")
            c1 = Cliente("user1", "Gerardo", "gerardo@gmail.com", "12345678")
            clientes.append(c1)
            print("Cliente creado:", 
                  "\nNombre:", c1.get_nombre(), "Correo:", c1.get_correo())

            # 2. Cliente inválido (correo malo)
            print("\n2. Intentando crear cliente con correo inválido...")
            try:
                c2 = Cliente("user2", "Ana", "correo_malo", "1234")
            except Exception as e:
                print("Error esperado:", e)

            # 3. Servicios
            print("\n3. Reservación valida de servicios...")
            s1 = AsesoriaAcademica("Asesoría", 5000.0)
            s2 = ReservaAuditorio("Auditorio", 10000.0)

            # 4. Reserva válida
            r1 = Reserva(c1, s1, 2)
            print(r1.procesar())
            reservas.append(r1)

            # 5. Reserva inválida
            print("\n5. Intentando reserva con duración negativa...")
            try:
                r2 = Reserva(c1, s2, -3)
                print(r2.procesar())
            except Exception as e:
                print("Error esperado:", e)

            # 6. Otra reserva válida
            print("\n6. Creando otra reserva válida...")
            r3 = Reserva(c1, s2, 3)
            print(r3.procesar())
            reservas.append(r3)

            # 7. Cambio de correo válido
            print("\n7. Cambiando correo a uno válido...")
            c1.set_correo("nuevo@gmail.com")
            print("Correo actualizado:", c1.get_correo())

            # 8. Cambio de correo inválido
            print("\n8. Intentando cambiar correo a uno inválido...")
            try:
                c1.set_correo("malcorreo")
            except Exception as e:
                print("Error esperado:", e)

            # 9. Mostrar reservas
            print("\n9. Mostrando reservas realizadas...")
            for r in reservas:
                print(r.procesar())

            # 10. Validación cliente
            print("\n10. Validando cliente...")
            print("Cliente válido:", c1.es_valido())

        except Exception as e:
            print("Error general:", e)

if __name__ == "__main__":
    app = App()
    app.menu_principal()
