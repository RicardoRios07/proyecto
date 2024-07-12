from Gestionproyectos.models.models import Colaboracion
from Gestionproyectos.conexion.colaboracion_conexion import (
    select_all_colaboraciones,
    select_colaboracion_por_id,
    crear_colaboracion,
    eliminar_colaboracion,
    actualizar_colaboracion
)

def servicio_colaboraciones_all():
    colaboraciones = select_all_colaboraciones()
    print("Salida colaboraciones", colaboraciones)
    return colaboraciones

def servicio_consultar_colaboracion_id(colaboracion_id: int):
    if colaboracion_id != 0:
        colaboracion = select_colaboracion_por_id(colaboracion_id)
        print(colaboracion)
        return colaboracion
    else:
        return select_all_colaboraciones()

def servicio_crear_colaboracion(id: int, usuario_id: int, proyecto_id: int):
    colaboracion = servicio_consultar_colaboracion_id(id)
    print(colaboracion)
    if not colaboracion:
        nueva_colaboracion = Colaboracion(id=id, usuario_id=usuario_id, proyecto_id=proyecto_id)
        return crear_colaboracion(nueva_colaboracion)
    else:
        return "La colaboración ya existe"

def servicio_eliminar_colaboracion(id: int):
    return eliminar_colaboracion(id)

def servicio_actualizar_colaboracion(id: int, usuario_id: int, proyecto_id: int):
    colaboracion = servicio_consultar_colaboracion_id(id)
    if colaboracion:
        colaboracion_actualizada = Colaboracion(id=id, usuario_id=usuario_id, proyecto_id=proyecto_id)
        return actualizar_colaboracion(colaboracion_actualizada)
    else:
        return "La colaboración no existe"