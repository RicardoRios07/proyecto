from Gestionproyectos.models.models import Tarea
from Gestionproyectos.conexion.tarea_conexion import (
    select_all_tareas,
    select_tarea_por_id,
    crear_tarea,
    eliminar_tarea,
    actualizar_tarea
)

def servicio_tareas_all():
    tareas = select_all_tareas()
    print("Salida tareas", tareas)
    return tareas

def servicio_consultar_tarea_id(tarea_id: int):
    if tarea_id != 0:
        tarea = select_tarea_por_id(tarea_id)
        print(tarea)
        return tarea
    else:
        return select_all_tareas()

def servicio_crear_tarea(id: int, nombre: str, descripcion: str, estado: str, proyecto_id: int, asignado_a: int):
    tarea = servicio_consultar_tarea_id(id)
    print(tarea)
    if not tarea:
        nueva_tarea = Tarea(id=id, nombre=nombre, descripcion=descripcion, estado=estado, proyecto_id=proyecto_id, asignado_a=asignado_a)
        return crear_tarea(nueva_tarea)
    else:
        return "La tarea ya existe"

def servicio_eliminar_tarea(id: int):
    return eliminar_tarea(id)

def servicio_actualizar_tarea(id: int, nombre: str, descripcion: str, estado: str, proyecto_id: int, asignado_a: int):
    tarea = servicio_consultar_tarea_id(id)
    if tarea:
        tarea_actualizada = Tarea(id=id, nombre=nombre, descripcion=descripcion, estado=estado, proyecto_id=proyecto_id, asignado_a=asignado_a)
        return actualizar_tarea(tarea_actualizada)
    else:
        return "La tarea no existe"