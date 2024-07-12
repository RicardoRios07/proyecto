from Gestionproyectos.models.models import Planificacion
from Gestionproyectos.conexion.conexion import connect
from sqlmodel import SQLModel, Session, select, create_engine
from sqlalchemy.exc import SQLAlchemyError

def select_all_planificaciones():
    engine = connect()
    with Session(engine) as session:
        consulta = select(Planificacion)
        planificaciones = session.exec(consulta)
        return planificaciones.all()

def select_planificacion_por_id(planificacion_id: int):
    engine = connect()
    with Session(engine) as session:
        consulta = select(Planificacion).where(Planificacion.id == planificacion_id)
        resultado = session.exec(consulta)
        return resultado.one_or_none()

def crear_planificacion(planificacion: Planificacion):
    engine = connect()
    try:
        with Session(engine) as session:
            session.add(planificacion)
            session.commit()
            if planificacion.id is not None:
                consulta = select(Planificacion).where(Planificacion.id == planificacion.id)
                resultado = session.exec(consulta)
                return resultado.one_or_none()
            else:
                return None
    except SQLAlchemyError as e:
        print(e)
        return None

def eliminar_planificacion(id: int):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Planificacion).where(Planificacion.id == id)
            planificacion = session.exec(consulta).one_or_none()
            if planificacion:
                session.delete(planificacion)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)
        return False

def actualizar_planificacion(planificacion: Planificacion):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Planificacion).where(Planificacion.id == planificacion.id)
            planificacion_actual = session.exec(consulta).one_or_none()
            if planificacion_actual:
                planificacion_actual.descripcion = planificacion.descripcion
                planificacion_actual.fecha_inicio = planificacion.fecha_inicio
                planificacion_actual.fecha_fin = planificacion.fecha_fin
                planificacion_actual.proyecto_id = planificacion.proyecto_id
                session.add(planificacion_actual)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)
        return False