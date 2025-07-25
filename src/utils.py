# ================================ LIBRERÍAS ================================ #
import streamlit as st
import datetime as dt


# ================================ FUNCIONES ================================ #
def time_to_seconds(t: dt.time) -> int:
    return t.hour * 3600 + t.minute * 60 + t.second


def seconds_to_time(s: int) -> dt.time:
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    # Opcional: ajusta por si supera 24 h (h %= 24)
    return dt.time(h % 24, m, sec)


def time_input_plus(label: str,
                    start: dt.time = dt.time(0, 0),
                    end: dt.time = dt.time(23, 59),
                    step_minutes: int = 15,
                    default: dt.time | None = None,
                    on_change=None,
                    key: str | None = None) -> dt.time | None:
    """
    Dada las limitaciones que tiene el método time_input propio de streamlit,
    se crea `time_input_plus` con la finalidad de imitar programas como
    google calendar. Esta función otorga opciones cada `step_minutes` y la
    posibilidad de teclear un valor personalizado HH:MM.

    Args:
        label (str): Texto de la etiqueta del widget.
        start (datetime.time): Hora de inicio (incluida).
        end (datetime.time): Hora de fin (incluida).
        step_minutes (int): Intervalo entre opciones en minutos.
        default (datetime.time): Valor por defecto seleccionado.
        key (str | None): Clave para Streamlit si hay múltiples widgets.

    Returns:
        datetime.time | None: Hora seleccionada o `None`.
    """

    # 1) Generar lista de cadenas "HH:MM" en pasos de step_minutes
    rangos_horas = []
    counter_time = time_to_seconds(start)
    final_time = time_to_seconds(end)

    while counter_time < final_time:
        rangos_horas.append(seconds_to_time(counter_time).strftime("%H:%M"))
        counter_time += step_minutes * 60

    # 2) Si default es None, obtiene el valor de start
    if default is None:
        default = start

    # 3) Determinar índice inicial
    try:
        idx = rangos_horas.index(default.strftime("%H:%M"))
    except ValueError:
        idx = 0

    # 4) Mostrar selectbox con entrada libre
    seleccion_str = st.selectbox(label, options=rangos_horas, index=idx,
                                 key=key+"_time_plus",
                                 accept_new_options=False, on_change=on_change)

    # 5) Validar y convertir a datetime.time
    try:
        h, m = map(int, seleccion_str.split(':'))
        return dt.time(h, m)
    except Exception:
        st.error(f"Formato inválido: «{seleccion_str}». Debe ser HH:MM.")
        return None
