from Gestionproyectos.models.models import Usuario
from Gestionproyectos.conexion.usuario_conexion import (
    select_all_usuarios,
    select_usuario_por_id,
    crear_usuario,
    eliminar_usuario,
    actualizar_usuario
)

def servicio_usuarios_all():
    usuarios = select_all_usuarios()
    print("Salida usuarios", usuarios)
    return usuarios

def servicio_consultar_usuario_id(usuario_id: int):
    if usuario_id != 0:
        usuario = select_usuario_por_id(usuario_id)
        print(usuario)
        return usuario
    else:
        return select_all_usuarios()

def servicio_crear_usuario(id: int, nombre: str, email: str, tipo: str):
    usuario = servicio_consultar_usuario_id(id)
    print(usuario)
    if not usuario:
        nuevo_usuario = Usuario(id=id, nombre=nombre, email=email, tipo=tipo)
        return crear_usuario(nuevo_usuario)
    else:
        return "El usuario ya existe"

def servicio_eliminar_usuario(id: int):
    return eliminar_usuario(id)

def servicio_actualizar_usuario(id: int, nombre: str, email: str, tipo: str):
    usuario = servicio_consultar_usuario_id(id)
    if usuario:
        usuario_actualizado = Usuario(id=id, nombre=nombre, email=email, tipo=tipo)
        return actualizar_usuario(usuario_actualizado)
    else:
        return "El usuario no existe"
