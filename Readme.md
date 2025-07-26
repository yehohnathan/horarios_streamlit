# Generador de Horarios en Streamlit 🗓️

![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-fc4c02?style=flat-square)
![Python >=3.10](https://img.shields.io/badge/Python-%E2%89%A53.10-blue?style=flat-square)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)

Generador de Horarios es una aplicación **interactiva** construida con
[Streamlit](https://streamlit.io/) que permite:

* Definir actividades, rango de días y horas, y asignarles color.
* Visualizar dichas actividades sobre una grilla horaria flexible.
* Ajustar la granularidad (minutos por bloque) y la ventana de horas mostradas
  en tiempo real.
* Limpiar celdas individuales mediante el sidebar.

> **Estado del proyecto:** MVP funcional orientado a la demostración de
> conceptos en Streamlit. Se anima a la comunidad a contribuir para alcanzar
> la visión descrita en la hoja de ruta.

---

## Tabla de contenidos

1. [Demo](#demo)
2. [Arquitectura](#arquitectura)
3. [Instalación](#instalación)
4. [Uso](#uso)
5. [Personalización](#personalización)
6. [Hoja de ruta](#hoja-de-ruta)
7. [Contribuciones](#contribuciones)
8. [Licencia](#licencia)

---

## Demo

| Interfaz principal               | Ajustes en el sidebar            |
| -------------------------------- | -------------------------------- |
| ![Main UI](<img width="1308" height="676" alt="Menu1" src="https://github.com/user-attachments/assets/fba337fc-0d51-4cf9-9a5c-d30bc0cf12a7" />
) | ![Sidebar](<img width="1303" height="678" alt="Menu2" src="https://github.com/user-attachments/assets/12d845bc-4023-4492-ad38-819774feb890" />
) |

---

## Arquitectura

```
.
├─ .streamlit/
│  └─ config.toml          # Tema claro por defecto
├─ models/
│  └─ HorarioStreamlit.py  # Lógica de negocio y UI
├─ utils.py                # Widgets y helpers de tiempo
├─ app.py                  # Punto de entrada Streamlit
└─ README.md
```

### Principales componentes

| Archivo                      | Rol                                                                   |
| ---------------------------- | --------------------------------------------------------------------- |
| **`HorarioStreamlit.py`**    | Clase con la lógica de tabla, validaciones y estilo.                  |
| **`utils.py`**               | Funciones auxiliares (`time_input_plus`, conversión tiempo⇄segundos). |
| **`app.py`**                 | Orquesta la página, configura el layout y llama a la clase.           |
| **`.streamlit/config.toml`** | Fuerza el tema claro (`base="light"`) y colores corporativos.         |

---

## Instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/<usuario>/generador‑horarios.git
cd generador‑horarios
```

2. **Crear entorno virtual**

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Ejecutar en local**

```bash
streamlit run app.py
```

> Si tu navegador no se abre automáticamente, visita
> `http://localhost:8501`.

---

## Uso

1. Completa **Actividad**, selecciona **Días**, **Desde**, **Hasta** y un
   **Color**.
2. Pulsa **Agregar**. Las celdas correspondientes se rellenarán con el nombre
   de la actividad (texto blanco y negrita) y el fondo indicado.
3. Ajusta en el **sidebar**:

   * **Minutos por bloque** → granularidad (1 – 60 min).
   * **Horas visibles** → sub‐rango horario mostrado.
   * **Reiniciar tabla** → regenera la grilla con los nuevos parámetros.
4. Para borrar, selecciona día y hora en el sidebar y pulsa
   **Limpiar celda**.

---

## Personalización

### Tema claro personalizado

El archivo `.streamlit/config.toml` define:

```toml
[theme]
base="light"
primaryColor="#1F77B4"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#000000"
font="sans serif"
```

Puedes adaptar la paleta al manual de identidad de tu organización.

### Columnas, fuentes y estilo

El módulo `HorarioStreamlit.py` aplica estilos mediante
`pandas.Styler`. Si deseas otra tipografía, modifica la sección
`header_styles` y la función `highlight`.

---

## Hoja de ruta 🔭

A continuación se presentan **líneas de mejora priorizadas**. La redacción
incluye el *por‑qué* y una **sugerencia técnica** para cada punto:

| Nº | Mejora propuesta                                | Motivación & Beneficio                                                                         | Sugerencia de implementación                                                                                                                                              |
| -- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1  | **Granularidad adaptativa**                     | Evitar “bloques vacíos” en rangos estrechos (p. ej. 08 h – 11 h) y reducir el scroll vertical. | Calcular `step_minutes` como mínimo común divisor de los intervalos registrados o permitir granularidad heterogénea mediante un segundo índice oculto.                    |
| 2  | **Ajuste automático de celdas no coincidentes** | Hoy, si la actividad no encaja exactamente en el grid, se crean filas “huérfanas”.             | Detectar desajuste y extender filas contiguas (merge), o bien dividir el bloque más cercano para absorver la fracción sobrante.                                           |
| 3  | **Widgets más intuitivos**                      | Reducir fricción al usuario final (especialmente en móvil).                                    | - Reemplazar `pills` por `st.multiselect` con etiquetas completas.<br>- Incluir iconos y tooltips.<br>- Validar en vivo con regex y feedback instantáneo.                 |
| 4  | **Exportación a Google Calendar & iCal**        | Facilitar la integración con calendarios corporativos.                                         | Utilizar [`google-api-python-client`](https://github.com/googleapis/google-api-python-client) y `ics.py`; generar un archivo `.ics` descargable y/o push via API OAuth 2. |
| 5  | **Múltiples actividades por celda**             | Reflejar escenarios con solapamiento (tareas paralelas).                                       | Convertir la celda en una lista (o badge stack) y desplegar con “hover” o ventana emergente; almacenar en `style_dict` una lista de colores.                              |
| 6  | **Persistencia multi‑sesión & multi‑usuario**   | Conservar horarios entre visitas y habilitar colaboración.                                     | Integrar SQLite/SQLModel o un servicio SAAS (Supabase, Firebase). Al cargar la app, recuperar el horario según el usuario autenticado (e‑mail, Google SSO).               |

Los *issues* se abren en la pestaña **️Issues** del repositorio. Pull
requests son bienvenidos 😉.

---

## Contribuciones

1. Haz un fork del proyecto.
2. Crea una rama: `git checkout -b feature/mi-mejora`.
3. Lanza tu código: `git commit -m "Añade tal funcionalidad"`.
4. Sube la rama: `git push origin feature/mi-mejora`.
5. Abre un **Pull Request** describiendo tu aportación.

Se agradece:

* Código limpio y documentado siguiendo **PEP 8 (79 c/car. máx.)**.
* Tests si el componente lo amerita.
* Comentarios en español o inglés consistentes.

---

## Licencia

Este proyecto se distribuye bajo licencia
[MIT](LICENSE). Eres libre de usar, modificar y distribuir el código siempre
que conserves la nota de copyright y la licencia.


---
