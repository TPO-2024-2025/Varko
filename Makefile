__venv_dir = .venv
__venv_marker = $(__venv_dir)/.marker
PYTHON = $(__venv_dir)/bin/python

default:
	$(MAKE) format
	$(MAKE) test
.PHONY: default

format: $(__venv_marker)
	$(PYTHON) -m black .
.PHONY: format

test: $(__venv_marker)
	$(PYTHON) -m unittest discover -s test -p "*_test.py" --verbose
.PHONY: test

start-%:
	# Home Assistant
	$(MAKE) .run/$*/home-assistant/config/custom_components
	rm -rf .run/$*/home-assistant/config/custom_components/varko
	cp -r src/custom_components/varko .run/$*/home-assistant/config/custom_components/varko
	$(MAKE) .run/$*/home-assistant/config/custom_components/varko/__pycache__
	$(MAKE) .run/$*/home-assistant/config/custom_components/varko/services/__pycache__

	# MQTT
	$(MAKE) .run/$*/mqtt/mosquitto/config
	rm -f .run/$*/mqtt/mosquitto/config/mosquitto.conf
	cp config/mosquitto/mosquitto.$*.conf .run/$*/mqtt/mosquitto/config/mosquitto.conf

	# Frigate
	$(MAKE) .run/$*/frigate/config
	rm -f .run/$*/frigate/config/config.yml
	cp config/frigate/config.$*.yaml .run/$*/frigate/config/config.yml

	docker compose --profile $* up -d

.run/%:
	mkdir -p $@
	chmod 777 $@

stop-%:
	docker compose --profile $* down

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
