test: venv/.requirements_installed
	. venv/bin/activate; pytest

venv/.requirements_installed: venv/bin/activate
	. venv/bin/activate; pip install --upgrade pip; pip install -q -r requirements.txt
	@touch venv/.requirements_installed

venv/bin/activate:
	python3 -m venv venv

clean:
	rm -Rf venv

.PHONY: clean test
