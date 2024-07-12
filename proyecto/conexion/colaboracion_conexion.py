from Gestionproyectos.models.models import Colaboracion
from Gestionproyectos.conexion.conexion import connect
from sqlmodel import SQLModel, Session, select, create_engine
from sqlalchemy.exc import SQLAlchemyError

def select_all_colaboraciones():
    engine = connect()
    with Session(engine) as session:
        consulta = select(Colaboracion)
        colaboraciones = session.exec(consulta)
        return colaboraciones.all()

def select_colaboracion_por_id(colaboracion_id: int):
    engine = connect()
    with Session(engine) as session:
        consulta = select(Colaboracion).where(Colaboracion.id == colaboracion_id)
        resultado = session.exec(consulta)
        return resultado.one_or_none()

def crear_colaboracion(colaboracion: Colaboracion):
    engine = connect()
    try:
        with Session(engine) as session:
            session.add(colaboracion)
            session.commit()
            if colaboracion.id is not None:
                consulta = select(Colaboracion).where(Colaboracion.id == colaboracion.id)
                resultado = session.exec(consulta)
                return resultado.one_or_none()
            else:
                return None
    except SQLAlchemyError as e:
        print(e)
        return None

def eliminar_colaboracion(id: int):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Colaboracion).where(Colaboracion.id == id)
            colaboracion = session.exec(consulta).one_or_none()
            if colaboracion:
                session.delete(colaboracion)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)
        return False

def actualizar_colaboracion(colaboracion: Colaboracion):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Colaboracion).where(Colaboracion.id == colaboracion.id)
            colaboracion_actual = session.exec(consulta).one_or_none()
            if colaboracion_actual:
                colaboracion_actual.usuario_id = colaboracion.usuario_id
                colaboracion_actual.proyecto_id = colaboracion.proyecto_id
                session.add(colaboracion_actual)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)
        return False