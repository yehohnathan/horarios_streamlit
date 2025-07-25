# src/app.py

import streamlit as st
from models.HorarioStreamlit import HorarioStreamlit

st.set_page_config(
            page_icon="🧊", layout='wide', initial_sidebar_state="collapsed",
            menu_items={'About': "# Fue divertido al inicio :>"},)


def main():

    st.markdown("<h1 style='text-align: center;'>Generador de horarios</h1>",
                unsafe_allow_html=True)

    horario = HorarioStreamlit()
    horario.menuOpciones()
    horario.tabla_semana()


if __name__ == "__main__":
    main()
