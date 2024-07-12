from Gestionproyectos.models.models import Proyecto
from Gestionproyectos.conexion.proyecto_conexion import (
    select_all_proyectos,
    select_proyecto_por_id,
    crear_proyecto,
    eliminar_proyecto,
    actualizar_proyecto
)

def servicio_proyectos_all():
    proyectos = select_all_proyectos()
    print("Salida proyectos", proyectos)
    return proyectos

def servicio_consultar_proyecto_id(proyecto_id: int):
    if proyecto_id != 0:
        proyecto = select_proyecto_por_id(proyecto_id)
        print(proyecto)
        return proyecto
    else:
        return select_all_proyectos()

def servicio_crear_proyecto(id: int, nombre: str, descripcion: str, lider_id: int):
    proyecto = servicio_consultar_proyecto_id(id)
    print(proyecto)
    if not proyecto:
        nuevo_proyecto = Proyecto(id=id, nombre=nombre, descripcion=descripcion, lider_id=lider_id)
        return crear_proyecto(nuevo_proyecto)
    else:
        return "El proyecto ya existe"

def servicio_eliminar_proyecto(id: int):
    return eliminar_proyecto(id)

def servicio_actualizar_proyecto(id: int, nombre: str, descripcion: str, lider_id: int):
    proyecto = servicio_consultar_proyecto_id(id)
    if proyecto:
        proyecto_actualizado = Proyecto(id=id, nombre=nombre, descripcion=descripcion, lider_id=lider_id)
        return actualizar_proyecto(proyecto_actualizado)
    else:
        return "El proyecto no existe"
