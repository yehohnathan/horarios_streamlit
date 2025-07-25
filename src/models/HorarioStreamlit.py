# ================================ LIBRERÍAS ================================ #
import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from utils import time_input_plus

# ========================= CLASE: HorarioStreamlit ========================= #
class HorarioStreamlit:
    """
    Descripción de la clase
    """
    def __init__(self):
        """
        Inicializa con un DataFrame y un título opcional.
        """
        pass

    def menuOpciones(self):          
        # Reparto las columnas para el menú de los horarios
        actividad, dias, desde, hasta, color = st.columns(
            spec=[2.5, 2.5, 1, 1, 1],
            vertical_alignment='top', gap=None, border=True)

        # Ingresar la actividad que piensa realizar
        with actividad:
            var_actividad = st.text_input(label="Actividad:")

        with dias:
            var_dias = st.pills(label="Días:", selection_mode="multi",
                                options= ["L", "K", "M", "J", "V", "S", "D"])

        with desde:
            var_desde = time_input_plus(
                label="Desde:",
                step_minutes=15,
                key="desde",
            )

        with hasta:
            var_hasta = time_input_plus(
                label="Hasta:",
                step_minutes=15,
                key="hasta",
            )

        with color:
            var_color = st.color_picker(label="Color:", value="#4233DC")
        



