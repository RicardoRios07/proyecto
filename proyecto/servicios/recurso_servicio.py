from Gestionproyectos.models.models import Recurso
from Gestionproyectos.conexion.recurso_conexion import (
    select_all_recursos,
    select_recurso_por_id,
    crear_recurso,
    eliminar_recurso,
    actualizar_recurso
)

def servicio_recursos_all():
    recursos = select_all_recursos()
    print("Salida recursos", recursos)
    return recursos

def servicio_consultar_recurso_id(recurso_id: int):
    if recurso_id != 0:
        recurso = select_recurso_por_id(recurso_id)
        print(recurso)
        return recurso
    else:
        return select_all_recursos()

def servicio_crear_recurso(id: int, proyecto_id: int, nombre: str, tipo: str):
    recurso = servicio_consultar_recurso_id(id)
    print(recurso)
    if not recurso:
        nuevo_recurso = Recurso(id=id, proyecto_id=proyecto_id, nombre=nombre, tipo=tipo)
        return crear_recurso(nuevo_recurso)
    else:
        return "El recurso ya existe"

def servicio_eliminar_recurso(id: int):
    return eliminar_recurso(id)

def servicio_actualizar_recurso(id: int, proyecto_id: int, nombre: str, tipo: str):
    recurso = servicio_consultar_recurso_id(id)
    if recurso:
        recurso_actualizado = Recurso(id=id, proyecto_id=proyecto_id, nombre=nombre, tipo=tipo)
        return actualizar_recurso(recurso_actualizado)
    else:
        return "El recurso no existe"