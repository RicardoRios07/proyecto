from Gestionproyectos.models.models import Avance
from Gestionproyectos.conexion.conexion import connect
from sqlmodel import SQLModel, Session, select, create_engine
from sqlalchemy.exc import SQLAlchemyError

def select_all_avances():
    engine = connect()
    with Session(engine) as session:
        consulta = select(Avance)
        avances = session.exec(consulta)
        return avances.all()

def select_avance_por_id(avance_id: int):
    engine = connect()
    with Session(engine) as session:
        consulta = select(Avance).where(Avance.id == avance_id)
        resultado = session.exec(consulta)
        return resultado.one_or_none()

def crear_avance(avance: Avance):
    engine = connect()
    try:
        with Session(engine) as session:
            session.add(avance)
            session.commit()
            if avance.id is not None:
                consulta = select(Avance).where(Avance.id == avance.id)
                resultado = session.exec(consulta)
                return resultado.one_or_none()
            else:
                return None
    except SQLAlchemyError as e:
        print(e)
        return None

def eliminar_avance(id: int):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Avance).where(Avance.id == id)
            avance = session.exec(consulta).one_or_none()
            if avance:
                session.delete(avance)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)
        return False


def actualizar_avance(avance: Avance):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Avance).where(Avance.id == avance.id)
            avance_actual = session.exec(consulta).one_or_none()
            if avance_actual:
                avance_actual.descripcion = avance.descripcion
                avance_actual.fecha = avance.fecha
                avance_actual.tarea_id = avance.tarea_id
                session.add(avance_actual)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)
        return False