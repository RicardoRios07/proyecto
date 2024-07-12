import reflex as rx
from Gestionproyectos.models.models import Avance
from Gestionproyectos.servicios.avance_servicio import (
    servicio_avances_all,
    servicio_consultar_avance_id,
    servicio_crear_avance,
    servicio_eliminar_avance,
    servicio_actualizar_avance
)

class AvanceState(rx.State):
    avances: list[Avance] = []
    buscar_id: int = 0

    @rx.background
    async def get_todos_avances(self):
        async with self:
            self.avances = servicio_avances_all()

    @rx.background
    async def get_avance_id(self):
        async with self:
            self.avances = servicio_consultar_avance_id(self.buscar_id)

    def buscar_onchange(self, value: str):
        self.buscar_id = int(value)

    @rx.background
    async def crear_avance(self, data: dict):
        async with self:
            try:
                nuevo_avance = Avance(
                    id=data.get('id'),
                    tarea_id=data.get('tarea_id'),
                    descripcion=data.get('descripcion'),
                    fecha=data.get('fecha')
                )
                self.avances.append(servicio_crear_avance(nuevo_avance))
            except Exception as e:
                print(e)

    @rx.background
    async def eliminar_avance(self, id: int):
        async with self:
            try:
                servicio_eliminar_avance(id)
                await self.get_todos_avances()
            except Exception as e:
                print(e)

@rx.page(route="/avances", title="Lista de Avances", on_load=AvanceState.get_todos_avances)
def avances_page() -> rx.Component:
    return rx.flex(
        rx.heading("Avances", title="Avances", size="5", center=True),
        rx.vstack(
            buscar_avance_id(),
            dialog_avance_form(),
            justify="center",
            style={"margin": "20px", 'width': "100%"},
        ),
        tabla_avances(AvanceState.avances),
        direction="column",
        justify="center",
        style={"margin": "auto", 'width': "100%"},
    )

def tabla_avances(lista_avances: list[Avance]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("ID"),
                rx.table.column_header_cell("Tarea ID"),
                rx.table.column_header_cell("Descripción"),
                rx.table.column_header_cell("Fecha"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(lista_avances, row_table_avance)
        ),
    )

def row_table_avance(avance: Avance) -> rx.Component:
    return rx.table.row(
        rx.table.cell(avance.id),
        rx.table.cell(avance.tarea_id),
        rx.table.cell(avance.descripcion),
        rx.table.cell(avance.fecha),
        rx.table.cell(
            rx.hstack(
                rx.button("Eliminar", on_click=lambda: AvanceState.eliminar_avance(avance.id)),
            )
        ),
    )

def buscar_avance_id() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="ID de Avance", on_change=AvanceState.buscar_onchange),
        rx.button("Buscar Avance", on_click=AvanceState.get_avance_id)
    )

def dialog_avance_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Crear Avance", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Avance"),
                crear_avance_form(),
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

def crear_avance_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="ID", name="id", style={"width": "100px"}, max_length=5),
            rx.input(placeholder="Tarea ID", name="tarea_id", type="number"),
            rx.input(placeholder="Descripción", name="descripcion"),
            rx.input(placeholder="Fecha", name="fecha", type="date"),
            rx.dialog.close(
                rx.button("Crear Avance", type="submit"),
            ),
        ),
        on_submit=AvanceState.crear_avance,
    )