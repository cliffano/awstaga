################################################################
# PieMaker: A Makefile for generating API clients using OpenAPI Generator
# https://github.com/cliffano/piemaker
################################################################

# The version of PieMaker
PIEMAKER_VERSION = 0.9.0-pre.0

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
export VIRTUAL_ENV := /opt/poetry-venv
export PATH := ${VIRTUAL_ENV}/bin:${POETRY_HOME}/bin:$(PATH)

################################################################
# Base targets

# CI target to be executed by CI/CD tool
ci: clean deps lint test coverage complexity doc package reinstall test-integration

# Ensure stage directory exists
stage:
	mkdir -p stage

# Remove all generated API clients code
clean:
	rm -rf stage *.lock *.egg-info build dist docs/ $(PACKAGE_NAME)/_pycache_/ $(PACKAGE_NAME)/*.pyc tests/_pycache_/ tests/*.pyc .coverage ~/.wily/ .pytest_cache/ .tox/ .mypy_cache/ .coverage.*

# Retrieve the dependencies
deps:
	python3 -m venv ${POETRY_HOME} && ${POETRY_HOME}/bin/pip install poetry --ignore-installed
	python3 -m venv ${VIRTUAL_ENV} && PATH=${POETRY_HOME}/bin/:$$PATH poetry install --no-root --compile

deps-extra:
	apt-get update
	apt-get install -y python3-venv

# Update Makefile to the latest version on origin's main branch
update-to-latest:
	curl https://raw.githubusercontent.com/cliffano/piemaker/main/src/Makefile-piemaker -o Makefile

# Update Makefile to the version defined in TARGET_PIEMAKER_VERSION parameter
update-to-version:
	curl https://raw.githubusercontent.com/cliffano/piemaker/v$(TARGET_PIEMAKER_VERSION)/src/Makefile-piemaker -o Makefile

################################################################
# Testing targets

lint: stage
	mkdir -p docs/lint/pylint/ docs/lint/pylint/
	pylint $(PACKAGE_NAME)/*.py $(PACKAGE_NAME)/models/*.py tests/*.py tests/models/*.py tests-integration/*.py
	pylint $(PACKAGE_NAME)/*.py $(PACKAGE_NAME)/models/*.py tests/*.py tests/models/*.py tests-integration/*.py --output-format=pylint_report.CustomJsonReporter > docs/lint/pylint/report.json
	pylint_report docs/lint/pylint/report.json -o docs/lint/pylint/index.html

complexity: stage
	mv poetry.lock  /tmp/poetry.lock || echo "No poetry.lock to backup..."
	rm -rf docs/complexity/wily/ && mkdir -p docs/complexity/wily/
	wily clean -y
	wily build $(PACKAGE_NAME)/
	wily report --format HTML --output docs/complexity/wily/index.html $(PACKAGE_NAME)/__init__.py
	wily list-metrics
	mv /tmp/poetry.lock poetry.lock || echo "No backup poetry.lock to restore..."

test:
	rm -rf docs/test/pytest/ && mkdir -p docs/test/pytest/
	pytest -v tests --html=docs/test/pytest/index.html --self-contained-html --capture=no

test-integration:
	rm -rf docs/test-integration/pytest/ && mkdir -p docs/test-integration/pytest/
	pytest -v tests-integration --html=docs/test-integration/pytest/index.html --self-contained-html --capture=no
	cd examples/ && ./$(PACKAGE_NAME)-cli.sh

coverage:
	rm -rf docs/coverage/coverage/ && mkdir -p docs/coverage/coverage/
	COVERAGE_FILE=.coverage.unit coverage run --source=./$(PACKAGE_NAME) -m unittest discover -s tests
	coverage combine
	coverage report
	coverage html

################################################################
# Release targets

release-major:
	rtk release --release-increment-type major

release-minor:
	rtk release --release-increment-type minor

release-patch:
	rtk release --release-increment-type patch

################################################################
# Package and publishing targets

install: package
	poetry install

uninstall:
	pip3 uninstall $(PACKAGE_NAME) -y

reinstall:
	make uninstall || echo "Nothing to uninstall..."
	make package install

package:
	poetry build

publish:
	poetry publish --username __token__ --password $(PASSWORD)

################################################################
# Documentation targets

doc: stage
	rm -rf docs/doc/sphinx/ && mkdir -p docs/doc/sphinx/
	sphinx-apidoc -o docs/doc/sphinx/ --full -H "$(PACKAGE_NAME)" -A "$(AUTHOR)" $(PACKAGE_NAME) && \
		cd docs/doc/sphinx/ && \
		make html && \
		cp -R _build/html/* ../../../docs/doc/sphinx/

################################################################

.PHONY: ci clean stage deps deps-extra doc release lint complexity test test-integration coverage install uninstall reinstall package publish
