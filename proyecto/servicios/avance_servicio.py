from Gestionproyectos.models.models import Avance
from Gestionproyectos.conexion.avance_conexion import (
    select_all_avances,
    select_avance_por_id,
    crear_avance,
    eliminar_avance,
    actualizar_avance
)

def servicio_avances_all():
    avances = select_all_avances()
    print("Salida avances", avances)
    return avances

def servicio_consultar_avance_id(avance_id: int):
    if avance_id != 0:
        avance = select_avance_por_id(avance_id)
        print(avance)
        return avance
    else:
        return select_all_avances()

def servicio_crear_avance(id: int, tarea_id: int, descripcion: str, fecha: str):
    avance = servicio_consultar_avance_id(id)
    print(avance)
    if not avance:
        nuevo_avance = Avance(id=id, tarea_id=tarea_id, descripcion=descripcion, fecha=fecha)
        return crear_avance(nuevo_avance)
    else:
        return "El avance ya existe"

def servicio_eliminar_avance(id: int):
    return eliminar_avance(id)

def servicio_actualizar_avance(id: int, tarea_id: int, descripcion: str, fecha: str):
    avance = servicio_consultar_avance_id(id)
    if avance:
        avance_actualizado = Avance(id=id, tarea_id=tarea_id, descripcion=descripcion, fecha=fecha)
        return actualizar_avance(avance_actualizado)
    else:
        return "El avance no existe"