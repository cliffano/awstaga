export POETRY_HOME := /opt/poetry
export VIRTUAL_ENV := /opt/poetry-venv
export PATH := ${VIRTUAL_ENV}/bin:${POETRY_HOME}/bin:$(PATH)

ci: clean deps-extra deps lint test coverage complexity doc package reinstall test-integration

# Exclude complexity due to complexity requiring no uncommited local change
dev: clean deps-extra deps lint test coverage doc package reinstall test-integration

clean:
	rm -rf stage *.lock *.egg-info build dist docs/ awstaga/_pycache_/ awstaga/*.pyc tests/_pycache_/ tests/*.pyc .coverage

stage:
	mkdir -p stage stage/ docs/

deps:
	python3 -m venv ${POETRY_HOME} && ${POETRY_HOME}/bin/pip install poetry --ignore-installed
	python3 -m venv ${VIRTUAL_ENV} && PATH=${POETRY_HOME}/bin/:$$PATH poetry install --no-root --compile

deps-extra:
	apt-get update
	apt-get install -y python3-venv

doc: stage
	rm -rf docs/doc/sphinx/ && mkdir -p docs/doc/sphinx/
	sphinx-apidoc -o stage/doc/sphinx/ --full -H "awstaga" -A "Cliffano Subagio" awstaga && \
		cd stage/doc/sphinx/ && \
		make html && \
		cp -R _build/html/* ../../../docs/doc/sphinx/

# Due to the difference in pre-release handling between Python setuptools and semver (which RTK supports),
# we have to massage the version number in conf/info.yaml before and after rtk release.
release-major:
	rtk release --release-increment-type major
	git commit conf/info.yaml -m "Switch version to Python setuptools versioning scheme"

release-minor:
	rtk release --release-increment-type minor
	git commit conf/info.yaml -m "Switch version to Python setuptools versioning scheme"

release-patch:
	rtk release --release-increment-type patch
	git commit conf/info.yaml -m "Switch version to Python setuptools versioning scheme"

lint: stage
	mkdir -p stage/lint/pylint/ docs/lint/pylint/
	pylint awstaga/*.py awstaga/models/*.py tests/*.py tests/models/*.py tests-integration/*.py
	pylint awstaga/*.py awstaga/models/*.py tests/*.py tests/models/*.py tests-integration/*.py --output-format=pylint_report.CustomJsonReporter > stage/lint/pylint/report.json
	pylint_report stage/lint/pylint/report.json -o docs/lint/pylint/index.html

complexity: stage
	wily build awstaga/
	wily report docs/complexity/wily/index.html

test:
	pytest -v tests --html=docs/test/pytest/index.html --self-contained-html

test-integration:
	rm -rf stage/test-integration/ && mkdir -p stage/test-integration/
	python3 -m unittest tests-integration/*.py
	cd examples/ && ./cli.sh

coverage:
	COVERAGE_FILE=.coverage.unit coverage run --source=./awstaga -m unittest discover -s tests
	coverage combine
	coverage report
	coverage html

install: package
	poetry install

uninstall:
	pip3 uninstall awstaga -y

reinstall:
	make uninstall || echo "Nothing to uninstall..."
	make clean deps package install

package:
	poetry build

publish:
	poetry publish --username __token__ --password $(PASSWORD)

.PHONY: ci dev clean stage deps deps-extra doc release lint complexity test test-integration coverage install uninstall reinstall package publish
