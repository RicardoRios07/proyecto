import reflex as rx
from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel

class Usuario(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    email: str
    tipo: str 

    def __init__(self, nombre: str, email: str, tipo: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombre = nombre
        self.email = email
        self.tipo = tipo

class Proyecto(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    descripcion: str
    lider_id: int = Field(foreign_key="usuario.id")
    tareas: List["Tarea"] = Relationship(back_populates="proyecto")
    colaboraciones: List["Colaboracion"] = Relationship(back_populates="proyecto")

    def __init__(self, nombre: str, descripcion: str, lider_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombre = nombre
        self.descripcion = descripcion
        self.lider_id = lider_id

class Tarea(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    descripcion: str
    estado: str  
    proyecto_id: int = Field(foreign_key="proyecto.id")
    proyecto: Optional[Proyecto] = Relationship(back_populates="tareas")
    asignado_a: Optional[int] = Field(foreign_key="usuario.id")
    avances: List["Avance"] = Relationship(back_populates="tarea")

    def __init__(self, nombre: str, descripcion: str, estado: str, proyecto_id: int, asignado_a: Optional[int] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado
        self.proyecto_id = proyecto_id
        self.asignado_a = asignado_a

class Colaboracion(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    proyecto_id: int = Field(foreign_key="proyecto.id")
    proyecto: Optional[Proyecto] = Relationship(back_populates="colaboraciones")

    def __init__(self, usuario_id: int, proyecto_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario_id = usuario_id
        self.proyecto_id = proyecto_id

class Avance(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tarea_id: int = Field(foreign_key="tarea.id")
    tarea: Optional[Tarea] = Relationship(back_populates="avances")
    descripcion: str
    fecha: str

    def __init__(self, tarea_id: int, descripcion: str, fecha: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tarea_id = tarea_id
        self.descripcion = descripcion
        self.fecha = fecha

class Recurso(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    proyecto_id: int = Field(foreign_key="proyecto.id")
    proyecto: Optional[Proyecto] = Relationship()
    nombre: str
    tipo: str  

    def __init__(self, proyecto_id: int, nombre: str, tipo: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proyecto_id = proyecto_id
        self.nombre = nombre
        self.tipo = tipo

class Planificacion(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    proyecto_id: int = Field(foreign_key="proyecto.id")
    proyecto: Optional[Proyecto] = Relationship()
    descripcion: str
    fecha_inicio: str
    fecha_fin: str

    def __init__(self, proyecto_id: int, descripcion: str, fecha_inicio: str, fecha_fin: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proyecto_id = proyecto_id
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
