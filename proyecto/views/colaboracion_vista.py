import reflex as rx
from Gestionproyectos.models.models import Colaboracion
from Gestionproyectos.servicios.colaboracion_servicio import (
    servicio_colaboraciones_all,
    servicio_consultar_colaboracion_id,
    servicio_crear_colaboracion,
    servicio_eliminar_colaboracion,
    servicio_actualizar_colaboracion
)

class ColaboracionState(rx.State):
    colaboraciones: list[Colaboracion] = []
    buscar_id: int = 0

    @rx.background
    async def get_todas_colaboraciones(self):
        async with self:
            self.colaboraciones = servicio_colaboraciones_all()

    @rx.background
    async def get_colaboracion_id(self):
        async with self:
            self.colaboraciones = servicio_consultar_colaboracion_id(self.buscar_id)

    def buscar_onchange(self, value: str):
        self.buscar_id = int(value)

    @rx.background
    async def crear_colaboracion(self, data: dict):
        async with self:
            try:
                nueva_colaboracion = Colaboracion(
                    id=data.get('id'),
                    usuario_id=data.get('usuario_id'),
                    proyecto_id=data.get('proyecto_id')
                )
                self.colaboraciones.append(servicio_crear_colaboracion(nueva_colaboracion))
            except Exception as e:
                print(e)

    @rx.background
    async def eliminar_colaboracion(self, id: int):
        async with self:
            try:
                servicio_eliminar_colaboracion(id)
                await self.get_todas_colaboraciones()
            except Exception as e:
                print(e)

@rx.page(route="/colaboraciones", title="Lista de Colaboraciones", on_load=ColaboracionState.get_todas_colaboraciones)
def colaboraciones_page() -> rx.Component:
    return rx.flex(
        rx.heading("Colaboraciones", title="Colaboraciones", size="5", center=True),
        rx.vstack(
            buscar_colaboracion_id(),
            dialog_colaboracion_form(),
            justify="center",
            style={"margin": "20px", 'width': "100%"},
        ),
        tabla_colaboraciones(ColaboracionState.colaboraciones),
        direction="column",
        justify="center",
        style={"margin": "auto", 'width': "100%"},
    )

def tabla_colaboraciones(lista_colaboraciones: list[Colaboracion]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("ID"),
                rx.table.column_header_cell("Usuario ID"),
                rx.table.column_header_cell("Proyecto ID"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(lista_colaboraciones, row_table_colaboracion)
        ),
    )

def row_table_colaboracion(colaboracion: Colaboracion) -> rx.Component:
    return rx.table.row(
        rx.table.cell(colaboracion.id),
        rx.table.cell(colaboracion.usuario_id),
        rx.table.cell(colaboracion.proyecto_id),
        rx.table.cell(
            rx.hstack(
                rx.button("Eliminar", on_click=lambda: ColaboracionState.eliminar_colaboracion(colaboracion.id)),
            )
        ),
    )

def buscar_colaboracion_id() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="ID de Colaboración", on_change=ColaboracionState.buscar_onchange),
        rx.button("Buscar Colaboración", on_click=ColaboracionState.get_colaboracion_id)
    )

def dialog_colaboracion_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Crear Colaboración", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Colaboración"),
                crear_colaboracion_form(),
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

def crear_colaboracion_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="ID", name="id", style={"width": "100px"}, max_length=5),
            rx.input(placeholder="Usuario ID", name="usuario_id", type="number"),
            rx.input(placeholder="Proyecto ID", name="proyecto_id", type="number"),
            rx.dialog.close(
                rx.button("Crear Colaboración", type="submit"),
            ),
        ),
        on_submit=ColaboracionState.crear_colaboracion,
    )