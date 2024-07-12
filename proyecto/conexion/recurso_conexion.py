from Gestionproyectos.models.models import Recurso
from Gestionproyectos.conexion.conexion import connect
from sqlmodel import SQLModel, Session, select, create_engine
from sqlalchemy.exc import SQLAlchemyError

def select_all_recursos():
    engine = connect()
    with Session(engine) as session:
        consulta = select(Recurso)
        recursos = session.exec(consulta)
        return recursos.all()

def select_recurso_por_id(recurso_id: int):
    engine = connect()
    with Session(engine) as session:
        consulta = select(Recurso).where(Recurso.id == recurso_id)
        resultado = session.exec(consulta)
        return resultado.one_or_none()

def crear_recurso(recurso: Recurso):
    engine = connect()
    try:
        with Session(engine) as session:
            session.add(recurso)
            session.commit()
            if recurso.id is not None:
                consulta = select(Recurso).where(Recurso.id == recurso.id)
                resultado = session.exec(consulta)
                return resultado.one_or_none()
            else:
                return None
    except SQLAlchemyError as e:
        print(e)
        return None

def eliminar_recurso(id: int):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Recurso).where(Recurso.id == id)
            recurso = session.exec(consulta).one_or_none()
            if recurso:
                session.delete(recurso)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)
        return False


def actualizar_recurso(recurso: Recurso):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Recurso).where(Recurso.id == recurso.id)
            recurso_actual = session.exec(consulta).one_or_none()
            if recurso_actual:
                recurso_actual.nombre = recurso.nombre
                recurso_actual.tipo = recurso.tipo
                recurso_actual.proyecto_id = recurso.proyecto_id
                session.add(recurso_actual)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)
        return False
