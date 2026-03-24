# Desarrollo local tras clonar: venv + editable + completions en el home.
.PHONY: help dev venv install-editable completions test

help:
	@echo "explain-errors — objetivos Make (desarrollo interno)"
	@echo ""
	@echo "  make dev              Entorno completo: venv + pip install -e . + completions (bash/zsh/fish → ~)."
	@echo "  make venv             Solo crea .venv/ e instala/actualiza pip (no instala el paquete)."
	@echo "  make install-editable Instala el proyecto en modo editable (requiere .venv existente)."
	@echo "  make completions      Copia completions al home (requiere explain instalado en .venv)."
	@echo "  make test             Ejecuta la suite con unittest (requiere .venv con el paquete instalado)."
	@echo ""
	@echo "Flujo típico tras git clone:  make dev && source .venv/bin/activate"
	@echo "Tests sin activar venv:       .venv/bin/python -m pytest tests/ -q   # si tenés pytest"
	@echo "Versión:                      .venv/bin/explain --version"

dev: venv install-editable completions
	@echo ""
	@echo "Listo. Activá el venv:  source .venv/bin/activate"
	@echo "O usá:  .venv/bin/explain --help"

venv:
	python3 -m venv .venv
	.venv/bin/pip install -U pip

install-editable:
	.venv/bin/pip install -e .

completions:
	.venv/bin/explain --install-shell-completions

test:
	.venv/bin/python -m unittest discover -s tests -v
