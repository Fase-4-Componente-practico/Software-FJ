#-----------------------------------------------
#  --- ARCHIVO: fj_services.py ---
# Define los servicios que ofrece el sistema. 
#-----------------------------------------------

from abc import ABC, abstractmethod

# =====================================================
# ---- CLASE BASE (ABSTRACTA) --------------------------
# Define la estructura común para todos los servicios,
# con el método abstracto calcular_costo.
# =====================================================
class Servicio(ABC):
    def __init__(self, nombre, costo_base):
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    # Método que debe implementar cada servicio. 
    # Se usa **kwargs para permitir recibir parámetros diferentes según el servicio. 
    def calcular_costo(self, cantidad, **kwargs):
        pass

#===========================================
# --- SERVICIO 1: Asesoría Académica ---
#===========================================
class AsesoriaAcademica(Servicio):
    
       
    def calcular_costo(self, cantidad, **kwargs):
        # Polimorfismo: incluye un recargo por modalidad grupal
        es_grupal = kwargs.get("es_grupal", False)      
        precio = self.costo_base * cantidad
        costo_final = precio * 1.20 if es_grupal else precio # Recargo del 20% para modalidad grupal
        return {
            "costo": costo_final,
            "detalle": "Modalidad Grupal (+20%)" if es_grupal else "Modalidad: Individual"
        }
    
    def describir_servicio(self):
        return "Asesorías académicas personalizadas por horas."

#===========================================
# --- SERVICIO 2: Reserva de Auditorio -----
#===========================================
class ReservaAuditorio(Servicio):
    
    def calcular_costo(self, cantidad, **kwargs):
        # Polimorfismo: incluye un cargo fijo adicional
        incluir_limpieza = kwargs.get("incluir_limpieza", True)
        cargo_extra = 15000 if incluir_limpieza else 0.0
        costo_final = (self.costo_base * cantidad) + cargo_extra
        
        return {
            "costo": costo_final,
            "detalle": "Incluye servicio de limpieza ($15,000)" if incluir_limpieza else "Sin servicio de limpieza"
        }
   
    def describir_servicio(self):
        return "Reserva de auditorios para eventos y reuniones por horas."

#===========================================
# --- SERVICIO 3: Préstamo de Equipo ---
#===========================================
class PrestamoEquipo(Servicio):
    def calcular_costo(self, cantidad,**kwargs):
        # Polimorfismo: descuento por cantidad de horas
        total = self.costo_base * cantidad
        descuento = False
        if cantidad > 5:
            total *= 0.90  # 10% descuento por mas de 5 horas
            descuento = True
        return {
            "costo": total,
            "detalle": "Descuento del 10% aplicado por mas de 5 horas " if descuento else "Sin descuento"
        }
    def describir_servicio(self):
        return "Préstamo de equipos tecnológicos por horas."
