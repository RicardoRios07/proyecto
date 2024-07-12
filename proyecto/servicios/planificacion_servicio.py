from Gestionproyectos.models.models import Planificacion
from Gestionproyectos.conexion.planificacion_conexion import (
    select_all_planificaciones,
    select_planificacion_por_id,
    crear_planificacion,
    eliminar_planificacion,
    actualizar_planificacion
)

def servicio_planificaciones_all():
    planificaciones = select_all_planificaciones()
    print("Salida planificaciones", planificaciones)
    return planificaciones

def servicio_consultar_planificacion_id(planificacion_id: int):
    if planificacion_id != 0:
        planificacion = select_planificacion_por_id(planificacion_id)
        print(planificacion)
        return planificacion
    else:
        return select_all_planificaciones()

def servicio_crear_planificacion(id: int, proyecto_id: int, descripcion: str, fecha_inicio: str, fecha_fin: str):
    planificacion = servicio_consultar_planificacion_id(id)
    print(planificacion)
    if not planificacion:
        nueva_planificacion = Planificacion(id=id, proyecto_id=proyecto_id, descripcion=descripcion, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
        return crear_planificacion(nueva_planificacion)
    else:
        return "La planificación ya existe"

def servicio_eliminar_planificacion(id: int):
    return eliminar_planificacion(id)

def servicio_actualizar_planificacion(id: int, proyecto_id: int, descripcion: str, fecha_inicio: str, fecha_fin: str):
    planificacion = servicio_consultar_planificacion_id(id)
    if planificacion:
        planificacion_actualizada = Planificacion(id=id, proyecto_id=proyecto_id, descripcion=descripcion, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
        return actualizar_planificacion(planificacion_actualizada)
    else:
        return "La planificación no existe"