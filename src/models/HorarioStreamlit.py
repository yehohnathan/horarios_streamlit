"""Módulo de interfaz para crear y visualizar un horario semanal en Streamlit.

Contiene la clase `HorarioStreamlit`, que ofrece:
- Un menú para agregar actividades con día, hora y color.
- Un método para inicializar y estilizar un DataFrame de bloques horarios.
- Un sidebar para ajustar granularidad y rango de horas.
"""

# ================================ LIBRERÍAS ================================ #
import datetime as dt
from typing import List, Dict
import pandas as pd
import streamlit as st
from utils import time_input_plus  # noqa: F401  # Widget custom de horas


# ========================= CLASE: HorarioStreamlit ========================= #
class HorarioStreamlit:
    """Componente de UI para la creación y edición de un horario."""

    def __init__(self) -> None:
        """Inicializa estado y valores por defecto."""
        self.var_actividad: str = ""
        self.var_color: str = ""
        self.var_dias: List[str] = []
        self.var_desde: dt.time | None = None
        self.var_hasta: dt.time | None = None

        # Paso en minutos para cada bloque (ajustable en sidebar)
        self.step_minutes: int = 15

        # Mapa de abreviaturas a nombres de día
        self.day_map: Dict[str, str] = {
            "L": "Lunes", "K": "Martes", "M": "Miércoles",
            "J": "Jueves", "V": "Viernes", "S": "Sábado",
            "D": "Domingo",
        }

    def init_tabla_semana(self, hora_min: int, hora_max: int,
                          step: int) -> None:
        """
        Crea y guarda en session_state un DataFrame con bloques
        desde `hora_min` hasta `hora_max` con pasos de `step` minutos.
        """
        bloques: List[str] = []
        for h in range(hora_min, hora_max + 1):
            for m in range(0, 60, step):
                inicio = dt.time(h, m)
                fin_dt = (
                    dt.datetime.combine(dt.date.today(), inicio)
                    + dt.timedelta(minutes=step - 1)
                )
                fin = fin_dt.time()
                bloques.append(
                    f"{inicio.strftime('%H:%M')}-"
                    f"{fin.strftime('%H:%M')}"
                )

        df = pd.DataFrame({"Hora": bloques})
        for nombre in self.day_map.values():
            df[nombre] = ""  # columna vacía para cada día

        # Guardar en sesión
        st.session_state["semana_df"] = df
        st.session_state["style_dict"] = {}

    def menuOpciones(self) -> None:  # noqa: N802
        """
        Muestra el formulario principal para agregar actividades y
        llama a `agregarActividad` cuando se presiona "Agregar".
        """
        cols = st.columns(
            spec=[2.9, 2.6, 1.5, 1.5, 0.6, 1],
            vertical_alignment="bottom",
            gap="medium",
            border=False,
        )
        actividad, dias, desde, hasta, color, agregar = cols

        with actividad:
            var_actividad = st.text_input(label="Actividad:")

        with dias:
            var_dias = st.pills(
                label="Días:",
                selection_mode="multi",
                options=list(self.day_map.keys()),
            )

        with desde:
            var_desde = time_input_plus(
                label="Desde:",
                step_minutes=self.step_minutes,
                default=dt.time(0, 0),
                key="desde",
            )

        with hasta:
            var_hasta = time_input_plus(
                label="Hasta:",
                step_minutes=self.step_minutes,
                default=dt.time(23, 0),
                key="hasta",
            )

        with color:
            var_color = st.color_picker(label="Color:", value="#4233DC")

        with agregar:
            if st.button("Agregar", type="primary"):
                # Almacenar entrada y procesar
                self.var_actividad = var_actividad
                self.var_dias = var_dias
                self.var_desde = var_desde
                self.var_hasta = var_hasta
                self.var_color = var_color
                self.agregarActividad()

    def agregarActividad(self) -> None:
        """
        Valida inputs y marca en el DataFrame los bloques correspondientes
        con texto y color.
        """
        # Validaciones básicas
        if not all([self.var_actividad,
                    self.var_dias,
                    self.var_desde,
                    self.var_hasta]):
            st.error("Complete todos los campos antes de agregar.")
            return

        if self.var_hasta <= self.var_desde:
            st.error("La hora final debe ser mayor que la de inicio.")
            return

        df = st.session_state["semana_df"]
        style_dict = st.session_state["style_dict"]

        # Índices de fila según minutos totales
        min_ini = (self.var_desde.hour * 60
                   + self.var_desde.minute)
        min_fin = (self.var_hasta.hour * 60
                   + self.var_hasta.minute)
        idx_ini = min_ini // self.step_minutes
        idx_fin = min_fin // self.step_minutes

        # Pintar cada bloque y día seleccionado
        for idx in range(idx_ini, idx_fin + 1):
            for d in self.var_dias:
                col = self.day_map[d]
                df.at[idx, col] = self.var_actividad
                style_dict[(idx, col)] = self.var_color

        # Actualizar sesión y notificar
        st.session_state["semana_df"] = df
        st.session_state["style_dict"] = style_dict
        st.success("Actividad agregada.")

    def tabla_semana(self) -> None:
        """
        Muestra la tabla con estilo y ofrece sidebar para configurar:
        - step_minutes
        - rango de horas
        - limpieza de celdas
        """
        # Sidebar: granularidad y rango de horas
        st.sidebar.subheader("Modificar la granularidad y rango de horas")
        self.step_minutes = st.sidebar.slider(
            "Minutos por bloque", 1, 60, self.step_minutes, step=1
        )
        hora_min, hora_max = st.sidebar.slider(
            "Horas visibles", 0, 23, (0, 23), step=1, format="%d h"
        )

        # Inicializar o reiniciar tabla si cambia configuración
        if ("semana_df" not in st.session_state
                or st.sidebar.button("Reiniciar tabla")):
            self.init_tabla_semana(hora_min, hora_max,
                                   self.step_minutes)

        df = st.session_state["semana_df"]
        style_dict = st.session_state["style_dict"]

        # Función de estilos para celdas con actividad
        def highlight(data: pd.DataFrame) -> pd.DataFrame:
            res = pd.DataFrame("", index=data.index,
                               columns=data.columns)
            for (i, col), c in style_dict.items():
                res.at[i, col] = (
                    f"background-color: {c}; "
                    "color: white; font-weight: bold"
                )
            return res

        # Estilo CSS para encabezados
        header_styles = [
            {
                "selector": "th",
                "props": [
                    ("background-color", "#4B8BBE"),
                    ("color", "white"),
                    ("font-weight", "bold"),
                    ("text-align", "center"),
                ],
            }
        ]

        # Renderizar tabla estilizada
        styled = (
            df.style
              .apply(highlight,
                     axis=None,
                     subset=list(self.day_map.values()))
              .set_table_styles(header_styles)
        )
        st.dataframe(styled, hide_index=True)

        # Sidebar: formulario para limpiar celdas
        st.sidebar.subheader("🗑 Quitar actividad")
        dia_q = st.sidebar.selectbox("Día",
                                     options=list(self.day_map.keys()))
        hora_q = st.sidebar.selectbox("Hora",
                                      options=df["Hora"].tolist())
        if st.sidebar.button("Limpiar celda"):
            fila = df.index[df["Hora"] == hora_q][0]
            df.at[fila, dia_q] = ""
            style_dict.pop((fila, dia_q), None)
            st.session_state["semana_df"] = df
            st.session_state["style_dict"] = style_dict
            st.success(f"Celda {dia_q} · {hora_q} limpiada.")
