_absolute_path := $(shell pwd)

.PHONY: dev_sync
dev_sync:
	pipenv sync --dev

.PHONY: dev
dev:
	pip install pipenv
	PIPENV_VENV_IN_PROJECT=true pipenv shell
	$(dev_sync)

.PHONY: sync
sync:
	pipenv sync

.PHONY: fmt
fmt:
	pipenv run fmt
	npx prettier --write .

.PHONY: lint
lint:
	pipenv run lint
	npx prettier --check .

.PHONY: vet
vet:
	pipenv run vet

.PHONY: install_setup
install_setup:
	pip3 install setuptools wheel

.PHONY: build
build:
	pip3 install setuptools wheel
	python3 setup.py build

.PHONY: install
install:
	pip3 install setuptools wheel
	pip3 install . -c requirements.txt

.PHONY: clean
clean:
	rm -rf build/
	rm -rf dist/

.PHONY: uninstall
uninstall:
	pip3 uninstall ddiff
