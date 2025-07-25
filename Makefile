# Variables configurables
PYTHON        := python3
VENV_DIR      := .venv
REQ_FILE      := requirements.txt
MAIN_APP      := src/app.py

# Rutas al entorno virtual
ACTIVATE      := $(VENV_DIR)/bin/activate
PIP           := . $(ACTIVATE) && pip

.PHONY: help venv install run clean

help:
	@echo "Uso:"
	@echo "  make venv     -> Crear el entorno virtual"
	@echo "  make install  -> Instalar dependencias"
	@echo "  make run      -> Ejecutar la aplicacion"
	@echo "  make clean    -> Eliminar el entorno y caches"

venv:
	@echo "-> Creando entorno virtual en '$(VENV_DIR)'..."
	@$(PYTHON) -m venv $(VENV_DIR)

install: venv
	@echo "-> Actualizando pip e instalando requerimientos..."
	@. $(ACTIVATE) && pip install --upgrade pip
	@. $(ACTIVATE) && pip install -r $(REQ_FILE)

run: install
	@echo "-> Iniciando Streamlit..."
	@. $(ACTIVATE) && streamlit run $(MAIN_APP)

clean:
	@echo "-> Eliminando entorno virtual y caches..."
	@rm -rf $(VENV_DIR) 
	@find . -type d -name "__pycache__" -exec rm -rf {} +

