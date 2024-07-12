import reflex as rx
from Gestionproyectos.models.models import Proyecto
from Gestionproyectos.servicios.proyecto_servicio import (
    servicio_proyectos_all,
    servicio_consultar_proyecto_id,
    servicio_crear_proyecto,
    servicio_eliminar_proyecto,
    servicio_actualizar_proyecto
)

class ProyectoState(rx.State):
    proyectos: list[Proyecto] = []
    buscar_id: int = 0

    @rx.background
    async def get_todos_proyectos(self):
        async with self:
            self.proyectos = servicio_proyectos_all()

    @rx.background
    async def get_proyecto_id(self):
        async with self:
            self.proyectos = servicio_consultar_proyecto_id(self.buscar_id)

    def buscar_onchange(self, value: str):
        self.buscar_id = int(value)

    @rx.background
    async def crear_proyecto(self, data: dict):
        async with self:
            try:
                # Extrae los valores del formulario
                id = int(data.get('id'))
                nombre = data.get('nombre')
                descripcion = data.get('descripcion')
                lider_id = int(data.get('lider_id'))
                print(f'Crear proyecto con id={id}, nombre={nombre}, descripcion={descripcion}, lider_id={lider_id}')
                # Llama al servicio con los valores extraídos
                resultado = servicio_crear_proyecto(id, nombre, descripcion, lider_id)
                if resultado == "El proyecto ya existe":
                    print(resultado)
                else:
                    self.proyectos.append(resultado)
            except Exception as e:
                print(e)

    @rx.background
    async def eliminar_proyecto(self, id: int):
        async with self:
            try:
                servicio_eliminar_proyecto(id)
                await self.get_todos_proyectos()
            except Exception as e:
                print(e)


@rx.page(route="/proyectos", title="Lista de Proyectos", on_load=ProyectoState.get_todos_proyectos)
def proyectos_page() -> rx.Component:
    return rx.flex(
        rx.heading("Proyectos", title="Proyectos", size="5", center=True),
        rx.vstack(
            buscar_proyecto_id(),
            dialog_proyecto_form(),
            justify="center",
            style={"margin": "20px", 'width': "100%"},
        ),
        tabla_proyectos(ProyectoState.proyectos),
        direction="column",
        justify="center",
        style={"margin": "auto", 'width': "100%"},
    )

def tabla_proyectos(lista_proyectos: list[Proyecto]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("ID"),
                rx.table.column_header_cell("Nombre"),
                rx.table.column_header_cell("Descripción"),
                rx.table.column_header_cell("Líder ID"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(lista_proyectos, row_table_proyecto)
        ),
    )

def row_table_proyecto(proyecto: Proyecto) -> rx.Component:
    return rx.table.row(
        rx.table.cell(proyecto.id),
        rx.table.cell(proyecto.nombre),
        rx.table.cell(proyecto.descripcion),
        rx.table.cell(proyecto.lider_id),
        rx.table.cell(
            rx.hstack(
                rx.button("Eliminar", on_click=lambda: ProyectoState.eliminar_proyecto(proyecto.id)),
            )
        ),
    )

def buscar_proyecto_id() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="ID de Proyecto", on_change=ProyectoState.buscar_onchange),
        rx.button("Buscar Proyecto", on_click=ProyectoState.get_proyecto_id)
    )

def dialog_proyecto_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Crear Proyecto", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Proyecto"),
                crear_proyecto_form(),
                justify="center",
                align="center",
                direction="column",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("Cancelar", variant="soft", color_scheme="red"),
                ),
                spacing="2",
                justify="end",
                margin_top="10px",
            ),
            style={"width": "400px"},
        ),
    )

def crear_proyecto_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="ID", name="id", style={"width": "100px"}, max_length=5),
            rx.input(placeholder="Nombre", name="nombre"),
            rx.input(placeholder="Descripción", name="descripcion"),
            rx.input(placeholder="Líder ID", name="lider_id", type="number"),
            rx.dialog.close(
                rx.button("Crear Proyecto", type="submit"),
            ),
        ),
        on_submit=ProyectoState.crear_proyecto,
    )
