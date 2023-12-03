export POETRY_HOME := /opt/poetry
export VIRTUAL_ENV := /opt/poetry-venv
export PATH := ${VIRTUAL_ENV}/bin:${POETRY_HOME}/bin:$(PATH)

ci: clean deps lint test coverage complexity doc package reinstall test-integration

clean:
	rm -rf stage *.lock *.egg-info build dist docs/ awstaga/_pycache_/ awstaga/*.pyc tests/_pycache_/ tests/*.pyc .coverage ~/.wily/ .pytest_cache/ .tox/ .mypy_cache/ .coverage.*

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
	sphinx-apidoc -o docs/doc/sphinx/ --full -H "awstaga" -A "Cliffano Subagio" awstaga && \
		cd docs/doc/sphinx/ && \
		make html && \
		cp -R _build/html/* ../../../docs/doc/sphinx/

# Due to the difference in pre-release handling between Python setuptools and semver (which RTK supports),
# we have to massage the version number in conf/info.yaml before and after rtk release.
release-major:
	rtk release --release-increment-type major

release-minor:
	rtk release --release-increment-type minor

release-patch:
	rtk release --release-increment-type patch

lint: stage
	mkdir -p docs/lint/pylint/ docs/lint/pylint/
	pylint awstaga/*.py awstaga/models/*.py tests/*.py tests/models/*.py tests-integration/*.py
	pylint awstaga/*.py awstaga/models/*.py tests/*.py tests/models/*.py tests-integration/*.py --output-format=pylint_report.CustomJsonReporter > docs/lint/pylint/report.json
	pylint_report docs/lint/pylint/report.json -o docs/lint/pylint/index.html

complexity: stage
	mv poetry.lock  /tmp/poetry.lock || echo "No poetry.lock to backup..."
	rm -rf docs/complexity/wily/ && mkdir -p docs/complexity/wily/
	wily clean -y
	wily build awstaga/
	wily report --format HTML --output docs/complexity/wily/index.html
	wily index
	mv /tmp/poetry.lock poetry.lock || echo "No backup poetry.lock to restore..."

test:
	rm -rf docs/test/pytest/ && mkdir -p docs/test/pytest/
	pytest -v tests --html=docs/test/pytest/index.html --self-contained-html --capture=no

test-integration:
	rm -rf docs/test-integration/pytest && mkdir -p docs/test-integration/pytest
	pytest -v tests-integration --html=docs/test-integration/pytest/index.html --self-contained-html --capture=no
	cd examples/ && ./awstaga-cli.sh

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
	make package install

package:
	poetry build

publish:
	poetry publish --username __token__ --password $(PASSWORD)

.PHONY: ci clean stage deps deps-extra doc release lint complexity test test-integration coverage install uninstall reinstall package publish
