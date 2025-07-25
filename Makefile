# Variables configurables
PYTHON        := python3
REQ_FILE      := requirements.txt
MAIN_APP      := src/app.py
TEST_APP	  := tests/test.py

# Rutas al entorno virtual
PIP           := . $(ACTIVATE) && pip

.PHONY: help venv install run clean

help:
	@echo "Uso:"
	@echo "  make venv     -> Crear el entorno virtual"
	@echo "  make install  -> Instalar dependencias"
	@echo "  make run      -> Ejecutar la aplicacion"
	@echo "  make clean    -> Eliminar el entorno y caches"


install:
	@echo "-> Actualizando pip e instalando requerimientos..."
	pip install --upgrade pip
	pip install -r $(REQ_FILE)

run:
	@echo "-> Iniciando Streamlit..."
	streamlit run $(MAIN_APP)

test:
	@echo "-> Iniciando Streamlit..."
	streamlit run $(TEST_APP)

clean:
	@echo "-> Eliminando entorno virtual y caches..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +

