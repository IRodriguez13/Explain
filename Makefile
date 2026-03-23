# Desarrollo local tras clonar: venv + editable + completions en el home.
.PHONY: dev venv install-editable completions test

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
