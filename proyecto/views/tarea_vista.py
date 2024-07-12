import reflex as rx
from Gestionproyectos.models.models import Tarea
from Gestionproyectos.servicios.tarea_servicio import (
    servicio_tareas_all,
    servicio_consultar_tarea_id,
    servicio_crear_tarea,
    servicio_eliminar_tarea,
    servicio_actualizar_tarea
)

class TareaState(rx.State):
    tareas: list[Tarea] = []
    buscar_id: int = 0

    @rx.background
    async def get_todas_tareas(self):
        async with self:
            self.tareas = servicio_tareas_all()

    @rx.background
    async def get_tarea_id(self):
        async with self:
            self.tareas = servicio_consultar_tarea_id(self.buscar_id)

    def buscar_onchange(self, value: str):
        self.buscar_id = int(value)

    @rx.background
    async def crear_tarea(self, data: dict):
        async with self:
            try:
                nueva_tarea = Tarea(
                    id=data.get('id'),
                    nombre=data.get('nombre'),
                    descripcion=data.get('descripcion'),
                    estado=data.get('estado'),
                    proyecto_id=data.get('proyecto_id'),
                    asignado_a=data.get('asignado_a')
                )
                self.tareas.append(servicio_crear_tarea(nueva_tarea))
            except Exception as e:
                print(e)

    @rx.background
    async def eliminar_tarea(self, id: int):
        async with self:
            try:
                servicio_eliminar_tarea(id)
                await self.get_todas_tareas()
            except Exception as e:
                print(e)

@rx.page(route="/tareas", title="Lista de Tareas", on_load=TareaState.get_todas_tareas)
def tareas_page() -> rx.Component:
    return rx.flex(
        rx.heading("Tareas", title="Tareas", size="5", center=True),
        rx.vstack(
            buscar_tarea_id(),
            dialog_tarea_form(),
            justify="center",
            style={"margin": "20px", 'width': "100%"},
        ),
        tabla_tareas(TareaState.tareas),
        direction="column",
        justify="center",
        style={"margin": "auto", 'width': "100%"},
    )

def tabla_tareas(lista_tareas: list[Tarea]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("ID"),
                rx.table.column_header_cell("Nombre"),
                rx.table.column_header_cell("Descripción"),
                rx.table.column_header_cell("Estado"),
                rx.table.column_header_cell("Proyecto ID"),
                rx.table.column_header_cell("Asignado A"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(lista_tareas, row_table_tarea)
        ),
    )

def row_table_tarea(tarea: Tarea) -> rx.Component:
    return rx.table.row(
        rx.table.cell(tarea.id),
        rx.table.cell(tarea.nombre),
        rx.table.cell(tarea.descripcion),
        rx.table.cell(tarea.estado),
        rx.table.cell(tarea.proyecto_id),
        rx.table.cell(tarea.asignado_a),
        rx.table.cell(
            rx.hstack(
                rx.button("Eliminar", on_click=lambda: TareaState.eliminar_tarea(tarea.id)),
            )
        ),
    )

def buscar_tarea_id() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="ID de Tarea", on_change=TareaState.buscar_onchange),
        rx.button("Buscar Tarea", on_click=TareaState.get_tarea_id)
    )

def dialog_tarea_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Crear Tarea", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Tarea"),
                crear_tarea_form(),
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

def crear_tarea_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="ID", name="id", style={"width": "100px"}, max_length=5),
            rx.input(placeholder="Nombre", name="nombre"),
            rx.input(placeholder="Descripción", name="descripcion"),
            rx.input(placeholder="Estado", name="estado"),
            rx.input(placeholder="Proyecto ID", name="proyecto_id", type="number"),
            rx.input(placeholder="Asignado A", name="asignado_a", type="number"),
            rx.dialog.close(
                rx.button("Crear Tarea", type="submit"),
            ),
        ),
        on_submit=TareaState.crear_tarea,
    )
