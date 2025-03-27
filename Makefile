__venv_dir = .venv
__venv_marker = $(__venv_dir)/.marker
PYTHON = $(__venv_dir)/bin/python

default:
	$(MAKE) format
.PHONY: default

format: | $(__venv_marker)
	$(PYTHON) -m black .
.PHONY: format

update-requirements: requirements.in | $(__venv_marker)
	$(PYTHON) -m pip install -U pip-tools
	$(PYTHON) -m piptools compile -U --resolver backtracking
.PHONY: update-requirements

$(__venv_marker): requirements.txt
	rm -rf $(__venv_dir)
	python3 -m venv $(__venv_dir)
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -Ur $<
	touch $@
