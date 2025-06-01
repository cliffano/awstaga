################################################################
# PieMaker: Makefile for building Python packages
# https://github.com/cliffano/piemaker
################################################################

# PieMaker's version number
PIEMAKER_VERSION = 1.10.0

################################################################
# User configuration variables
# These variables should be stored in piemaker.yml config file,
# and they will be parsed using yq https://github.com/mikefarah/yq
# Example:
# ---
# package_name: somepackage
# author: Some Author

# PACKAGE_NAME is the name of the Python package
PACKAGE_NAME=$(shell yq .package_name piemaker.yml)

# AUTHOR is the author of the Python package
AUTHOR ?= $(shell yq .author piemaker.yml)

$(info ################################################################)
$(info Building Python package using PieMaker with user configurations:)
$(info - Package name: ${PACKAGE_NAME})
$(info - Author: ${AUTHOR})

export POETRY_HOME := /opt/poetry
export VIRTUAL_ENV := .venv
export PATH := ${VIRTUAL_ENV}/bin:${POETRY_HOME}/bin:$(PATH)

define python_venv
	. .venv/bin/activate && $(1)
endef

################################################################
# Base targets

# CI target to be executed by CI/CD tool
all:ci
ci: clean deps style lint test coverage complexity doc package reinstall test-integration

# Ensure stage directory exists
stage:
	mkdir -p stage

# Remove all temporary (staged, generated, cached) files
clean:
	rm -rf stage/ *.lock *.egg-info build dist/ docs/ $(PACKAGE_NAME)/__pycache__/ $(PACKAGE_NAME)/*.pyc tests/__pycache__/ tests/*.pyc .coverage ~/.wily/ .pytest_cache/ .tox/ .mypy_cache/ .coverage.*

# Retrieve the Pyhon package dependencies
deps:
	python3 -m venv ${POETRY_HOME} && ${POETRY_HOME}/bin/pip install --force-reinstall poetry==2.1.3 --ignore-installed
	python3 -m venv ${VIRTUAL_ENV} && PATH=${POETRY_HOME}/bin/:$$PATH poetry install --no-root --compile
	python3 -m venv ${POETRY_HOME} && ${POETRY_HOME}/bin/pip install --force-reinstall poetry-plugin-up==0.9.0 --ignore-installed
	$(call python_venv,poetry self add poetry-plugin-export)
	$(call python_venv,poetry export -f requirements.txt --without-hashes --with dev --output requirements.txt)

deps-upgrade:
	$(call python_venv,poetry up --latest)

deps-extra-apt:
	apt-get update
	apt-get install -y python3-venv
	apt-get install -y python3-sphinx # needed by sphinx-apidoc

rmdeps:
	rm -f poetry.lock requirements.txt
	rm -rf .venv/

# Update Makefile to the latest version tag
update-to-latest: TARGET_PIEMAKER_VERSION = $(shell curl -s https://api.github.com/repos/cliffano/piemaker/tags | jq -r '.[0].name')
update-to-latest: update-to-version

# Update Makefile to the main branch
update-to-main:
	curl https://raw.githubusercontent.com/cliffano/piemaker/main/src/Makefile-piemaker -o Makefile

# Update Makefile to the version defined in TARGET_PIEMAKER_VERSION parameter
update-to-version:
	curl https://raw.githubusercontent.com/cliffano/piemaker/$(TARGET_PIEMAKER_VERSION)/src/Makefile-piemaker -o Makefile

################################################################
# Formatting targets

style:
	$(call python_venv,black $(PACKAGE_NAME) tests tests-integration examples)

################################################################
# Testing targets

lint: stage
	rm -rf docs/lint/pylint/ stage/lint/ && mkdir -p docs/lint/pylint/ stage/lint/
	$(call python_venv,pylint $(shell find $(PACKAGE_NAME) -type f -regex ".*\.py" | xargs echo) $(shell find tests/ -type f -regex ".*\.py" | xargs echo) $(shell find tests-integration/ -type f -regex ".*\.py" | xargs echo))
	$(call python_venv,pylint $(shell find $(PACKAGE_NAME) -type f -regex ".*\.py" | xargs echo) $(shell find tests/ -type f -regex ".*\.py" | xargs echo) $(shell find tests-integration/ -type f -regex ".*\.py" | xargs echo) --output-format=pylint_report.CustomJsonReporter > docs/lint/pylint/report.json)
	$(call python_venv,pylint_report docs/lint/pylint/report.json -o docs/lint/pylint/index.html)

complexity: stage
	rm -rf docs/complexity/wily/ stage/complexity/ && mkdir -p docs/complexity/wily/ stage/complexity/
	$(call python_venv,wily clean -y)
	$(call python_venv,wily build $(PACKAGE_NAME)/)
	$(call python_venv,wily report --format HTML --output docs/complexity/wily/index.html $(PACKAGE_NAME)/__init__.py)
	$(call python_venv,wily list-metrics)

test:
	rm -rf docs/test/pytest/ stage/test/ && mkdir -p docs/test/pytest/ stage/test/
	$(call python_venv,pytest -v tests --html=docs/test/pytest/index.html --self-contained-html --capture=no)

test-integration:
	rm -rf docs/test-integration/pytest/ stage/test-integration/ && mkdir -p docs/test-integration/pytest/ stage/test-integration/
	$(call python_venv,pytest -v tests-integration --html=docs/test-integration/pytest/index.html --self-contained-html --capture=no)

test-examples:
	cd examples && \
	for f in *.sh; do \
	  bash -x "$$f"; \
	done

coverage:
	rm -rf docs/coverage/coverage/ stage/coverage/ && mkdir -p docs/coverage/coverage/ stage/coverage/
	$(call python_venv,COVERAGE_FILE=.coverage.unit coverage run --source=./$(PACKAGE_NAME) -m unittest discover -s tests)
	$(call python_venv,coverage combine)
	$(call python_venv,coverage report)
	$(call python_venv,coverage html && rm -f docs/coverage/coverage/.gitignore)

################################################################
# Release targets

release-major:
	rtk release --release-increment-type major

release-minor:
	rtk release --release-increment-type minor

release-patch:
	rtk release --release-increment-type patch

################################################################
# Packaging, installation, and publishing targets

package:
	$(call python_venv,poetry build)

install: package
	$(call python_venv,poetry install)

install-wheel: package
	$(call python_venv,pip3 install dist/$(PACKAGE_NAME)-*.whl)

uninstall:
	$(call python_venv,pip3 uninstall $(PACKAGE_NAME) -y || echo "Nothing to uninstall...")

reinstall: uninstall install

publish:
	$(call python_venv,poetry publish --username __token__ --password $(PASSWORD))

################################################################
# Documentation targets

doc: stage
	rm -rf docs/doc/sphinx/ stage/doc/ && mkdir -p docs/doc/sphinx/ stage/doc/
	$(call python_venv,sphinx-apidoc -o docs/doc/sphinx/ --full -H "$(PACKAGE_NAME)" -A "$(AUTHOR)" $(PACKAGE_NAME) && \
		cd docs/doc/sphinx/ && \
		make html && \
		cp -R _build/html/* ../../../docs/doc/sphinx/)

################################################################

.PHONY: all ci clean complexity configurations coverage deps deps-extra-apt deps-upgrade rmdeps doc export export export install install-wheel lint name package package publish reinstall release-major release-minor release-patch stage style test test-examples test-integration uninstall update-to-latest update-to-latest update-to-main update-to-version