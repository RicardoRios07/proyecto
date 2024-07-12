from Gestionproyectos.models.models import Tarea
from Gestionproyectos.conexion.conexion import connect
from sqlmodel import SQLModel, Session, select, create_engine
from sqlalchemy.exc import SQLAlchemyError

def select_all_tareas():
    engine = connect()
    with Session(engine) as session:
        consulta = select(Tarea)
        tareas = session.exec(consulta)
        return tareas.all()

def select_tarea_por_id(tarea_id: int):
    engine = connect()
    with Session(engine) as session:
        consulta = select(Tarea).where(Tarea.id == tarea_id)
        resultado = session.exec(consulta)
        return resultado.one_or_none()

def crear_tarea(tarea: Tarea):
    engine = connect()
    try:
        with Session(engine) as session:
            session.add(tarea)
            session.commit()
            if tarea.id is not None:
                consulta = select(Tarea).where(Tarea.id == tarea.id)
                resultado = session.exec(consulta)
                return resultado.one_or_none()
            else:
                return None
    except SQLAlchemyError as e:
        print(e)
        return None

def eliminar_tarea(id: int):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Tarea).where(Tarea.id == id)
            tarea = session.exec(consulta).one_or_none()
            if tarea:
                session.delete(tarea)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)
        return False

def actualizar_tarea(tarea: Tarea):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Tarea).where(Tarea.id == tarea.id)
            tarea_actual = session.exec(consulta).one_or_none()
            if tarea_actual:
                tarea_actual.nombre = tarea.nombre
                tarea_actual.descripcion = tarea.descripcion
                tarea_actual.estado = tarea.estado
                tarea_actual.proyecto_id = tarea.proyecto_id
                tarea_actual.asignado_a = tarea.asignado_a
                session.add(tarea_actual)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)
        return False