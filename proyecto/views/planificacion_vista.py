import reflex as rx
from Gestionproyectos.models.models import Planificacion
from Gestionproyectos.servicios.planificacion_servicio import (
    servicio_planificaciones_all,
    servicio_consultar_planificacion_id,
    servicio_crear_planificacion,
    servicio_eliminar_planificacion,
    servicio_actualizar_planificacion
)

class PlanificacionState(rx.State):
    planificaciones: list[Planificacion] = []
    buscar_id: int = 0

    @rx.background
    async def get_todas_planificaciones(self):
        async with self:
            self.planificaciones = servicio_planificaciones_all()

    @rx.background
    async def get_planificacion_id(self):
        async with self:
            self.planificaciones = servicio_consultar_planificacion_id(self.buscar_id)

    def buscar_onchange(self, value: str):
        self.buscar_id = int(value)

    @rx.background
    async def crear_planificacion(self, data: dict):
        async with self:
            try:
                nueva_planificacion = Planificacion(
                    id=data.get('id'),
                    proyecto_id=data.get('proyecto_id'),
                    descripcion=data.get('descripcion'),
                    fecha_inicio=data.get('fecha_inicio'),
                    fecha_fin=data.get('fecha_fin')
                )
                self.planificaciones.append(servicio_crear_planificacion(nueva_planificacion))
            except Exception as e:
                print(e)

    @rx.background
    async def eliminar_planificacion(self, id: int):
        async with self:
            try:
                servicio_eliminar_planificacion(id)
                await self.get_todas_planificaciones()
            except Exception as e:
                print(e)

@rx.page(route="/planificaciones", title="Lista de Planificaciones", on_load=PlanificacionState.get_todas_planificaciones)
def planificaciones_page() -> rx.Component:
    return rx.flex(
        rx.heading("Planificaciones", title="Planificaciones", size="5", center=True),
        rx.vstack(
            buscar_planificacion_id(),
            dialog_planificacion_form(),
            justify="center",
            style={"margin": "20px", 'width': "100%"},
        ),
        tabla_planificaciones(PlanificacionState.planificaciones),
        direction="column",
        justify="center",
        style={"margin": "auto", 'width': "100%"},
    )

def tabla_planificaciones(lista_planificaciones: list[Planificacion]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("ID"),
                rx.table.column_header_cell("Proyecto ID"),
                rx.table.column_header_cell("Descripción"),
                rx.table.column_header_cell("Fecha Inicio"),
                rx.table.column_header_cell("Fecha Fin"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(lista_planificaciones, row_table_planificacion)
        ),
    )

def row_table_planificacion(planificacion: Planificacion) -> rx.Component:
    return rx.table.row(
        rx.table.cell(planificacion.id),
        rx.table.cell(planificacion.proyecto_id),
        rx.table.cell(planificacion.descripcion),
        rx.table.cell(planificacion.fecha_inicio),
        rx.table.cell(planificacion.fecha_fin),
        rx.table.cell(
            rx.hstack(
                rx.button("Eliminar", on_click=lambda: PlanificacionState.eliminar_planificacion(planificacion.id)),
            )
        ),
    )

def buscar_planificacion_id() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="ID de Planificación", on_change=PlanificacionState.buscar_onchange),
        rx.button("Buscar Planificación", on_click=PlanificacionState.get_planificacion_id)
    )

def dialog_planificacion_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Crear Planificación", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Planificación"),
                crear_planificacion_form(),
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

def crear_planificacion_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="ID", name="id", style={"width": "100px"}, max_length=5),
            rx.input(placeholder="Proyecto ID", name="proyecto_id", type="number"),
            rx.input(placeholder="Descripción", name="descripcion"),
            rx.input(placeholder="Fecha Inicio", name="fecha_inicio", type="date"),
            rx.input(placeholder="Fecha Fin", name="fecha_fin", type="date"),
            rx.dialog.close(
                rx.button("Crear Planificación", type="submit"),
            ),
        ),
        on_submit=PlanificacionState.crear_planificacion,
    )