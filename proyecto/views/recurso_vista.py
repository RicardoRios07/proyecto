import reflex as rx
from Gestionproyectos.models.models import Recurso
from Gestionproyectos.servicios.recurso_servicio import (
    servicio_recursos_all,
    servicio_consultar_recurso_id,
    servicio_crear_recurso,
    servicio_eliminar_recurso,
    servicio_actualizar_recurso
)

class RecursoState(rx.State):
    recursos: list[Recurso] = []
    buscar_id: int = 0

    @rx.background
    async def get_todos_recursos(self):
        async with self:
            self.recursos = servicio_recursos_all()

    @rx.background
    async def get_recurso_id(self):
        async with self:
            self.recursos = servicio_consultar_recurso_id(self.buscar_id)

    def buscar_onchange(self, value: str):
        self.buscar_id = int(value)

    @rx.background
    async def crear_recurso(self, data: dict):
        async with self:
            try:
                nuevo_recurso = Recurso(
                    id=data.get('id'),
                    proyecto_id=data.get('proyecto_id'),
                    nombre=data.get('nombre'),
                    tipo=data.get('tipo')
                )
                self.recursos.append(servicio_crear_recurso(nuevo_recurso))
            except Exception as e:
                print(e)

    @rx.background
    async def eliminar_recurso(self, id: int):
        async with self:
            try:
                servicio_eliminar_recurso(id)
                await self.get_todos_recursos()
            except Exception as e:
                print(e)

@rx.page(route="/recursos", title="Lista de Recursos", on_load=RecursoState.get_todos_recursos)
def recursos_page() -> rx.Component:
    return rx.flex(
        rx.heading("Recursos", title="Recursos", size="5", center=True),
        rx.vstack(
            buscar_recurso_id(),
            dialog_recurso_form(),
            justify="center",
            style={"margin": "20px", 'width': "100%"},
        ),
        tabla_recursos(RecursoState.recursos),
        direction="column",
        justify="center",
        style={"margin": "auto", 'width': "100%"},
    )

def tabla_recursos(lista_recursos: list[Recurso]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("ID"),
                rx.table.column_header_cell("Proyecto ID"),
                rx.table.column_header_cell("Nombre"),
                rx.table.column_header_cell("Tipo"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(lista_recursos, row_table_recurso)
        ),
    )

def row_table_recurso(recurso: Recurso) -> rx.Component:
    return rx.table.row(
        rx.table.cell(recurso.id),
        rx.table.cell(recurso.proyecto_id),
        rx.table.cell(recurso.nombre),
        rx.table.cell(recurso.tipo),
        rx.table.cell(
            rx.hstack(
                rx.button("Eliminar", on_click=lambda: RecursoState.eliminar_recurso(recurso.id)),
            )
        ),
    )

def buscar_recurso_id() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="ID de Recurso", on_change=RecursoState.buscar_onchange),
        rx.button("Buscar Recurso", on_click=RecursoState.get_recurso_id)
    )

def dialog_recurso_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Crear Recurso", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Recurso"),
                crear_recurso_form(),
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

def crear_recurso_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="ID", name="id", style={"width": "100px"}, max_length=5),
            rx.input(placeholder="Proyecto ID", name="proyecto_id", type="number"),
            rx.input(placeholder="Nombre", name="nombre"),
            rx.input(placeholder="Tipo", name="tipo"),
            rx.dialog.close(
                rx.button("Crear Recurso", type="submit"),
            ),
        ),
        on_submit=RecursoState.crear_recurso,
    )
