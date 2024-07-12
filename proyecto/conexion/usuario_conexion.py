from Gestionproyectos.models.models import Usuario
from Gestionproyectos.conexion.conexion import connect
from sqlmodel import SQLModel, Session, select, create_engine
from sqlalchemy.exc import SQLAlchemyError

def select_all_usuarios():
    engine = connect()
    with Session(engine) as session:
        consulta = select(Usuario)
        usuarios = session.exec(consulta)
        return usuarios.all()

def select_usuario_por_id(usuario_id: int):
    engine = connect()
    with Session(engine) as session:
        consulta = select(Usuario).where(Usuario.id == usuario_id)
        resultado = session.exec(consulta)
        return resultado.one_or_none()

def crear_usuario(usuario: Usuario):
    engine = connect()
    try:
        with Session(engine) as session:
            session.add(usuario)
            session.commit()
            if usuario.id is not None:
                consulta = select(Usuario).where(Usuario.id == usuario.id)
                resultado = session.exec(consulta)
                return resultado.one_or_none()
            else:
                return None
    except SQLAlchemyError as e:
        print(e)
        return None

def eliminar_usuario(id: int):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Usuario).where(Usuario.id == id)
            usuario = session.exec(consulta).one_or_none()
            if usuario:
                session.delete(usuario)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)
        return False

def actualizar_usuario(usuario: Usuario):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Usuario).where(Usuario.id == usuario.id)
            usuario_actual = session.exec(consulta).one_or_none()
            if usuario_actual:
                usuario_actual.nombre = usuario.nombre
                usuario_actual.email = usuario.email
                usuario_actual.tipo = usuario.tipo
                session.add(usuario_actual)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)
        return False