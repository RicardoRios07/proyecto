from Gestionproyectos.models.models import Proyecto
from Gestionproyectos.conexion.conexion import connect
from sqlmodel import SQLModel, Session, select, create_engine
from sqlalchemy.exc import SQLAlchemyError

def select_all_proyectos():
    engine = connect()
    with Session(engine) as session:
        consulta = select(Proyecto)
        proyectos = session.exec(consulta)
        return proyectos.all()

def select_proyecto_por_id(proyecto_id: int):
    engine = connect()
    with Session(engine) as session:
        consulta = select(Proyecto).where(Proyecto.id == proyecto_id)
        resultado = session.exec(consulta)
        return resultado.one_or_none()

def crear_proyecto(proyecto: Proyecto):
    engine = connect()
    try:
        with Session(engine) as session:
            session.add(proyecto)
            session.commit()
            if proyecto.id is not None:
                consulta = select(Proyecto).where(Proyecto.id == proyecto.id)
                resultado = session.exec(consulta)
                return resultado.one_or_none()
            else:
                return None
    except SQLAlchemyError as e:
        print(e)
        return None

def eliminar_proyecto(id: int):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Proyecto).where(Proyecto.id == id)
            proyecto = session.exec(consulta).one_or_none()
            if proyecto:
                session.delete(proyecto)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)
        return False

def actualizar_proyecto(proyecto: Proyecto):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Proyecto).where(Proyecto.id == proyecto.id)
            proyecto_actual = session.exec(consulta).one_or_none()
            if proyecto_actual:
                proyecto_actual.nombre = proyecto.nombre
                proyecto_actual.descripcion = proyecto.descripcion
                proyecto_actual.lider_id = proyecto.lider_id
                session.add(proyecto_actual)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)
        return False