version=`yq -r .version conf/info.yaml`

ci: clean deps lint test coverage complexity doc package reinstall test-integration
dev: clean deps lint test coverage doc package reinstall test-integration

clean:
	rm -rf stage *.egg-info build dist docs/ __pycache__/ awstaga/__pycache__/ awstaga/*.pyc tests/__pycache__/ tests/*.pyc tests-integration/__pycache__/ tests-integration/*.pyc .coverage .pytest_cache/

stage:
	mkdir -p stage stage/ docs/

deps:
	pip3 install --ignore-installed -r requirements.txt
	pip3 install --ignore-installed -r requirements-dev.txt

deps-extra:
	apt-get install jq

doc: stage
	rm -rf docs/doc/sphinx/ && mkdir -p docs/doc/sphinx/
	sphinx-apidoc -o stage/doc/sphinx/ --full -H "awstaga" -A "Cliffano Subagio" awstaga && \
		cd stage/doc/sphinx/ && \
		make html && \
		cp -R _build/html/* ../../../docs/doc/sphinx/

# Due to the difference in pre-release handling between Python setuptools and semver (which RTK supports),
# we have to massage the version number in conf/info.yaml before and after rtk release.
release:
	sed -i '' -e 's/rc0/-rc0/' conf/info.yaml
	rtk release
	sed -i '' -e 's/-rc0.0/rc0/' conf/info.yaml
	git commit conf/info.yaml -m "Switch version to Python setuptools versioning scheme"

################################################################################
# Test targets
################################################################################

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
	examples/cli.sh

coverage:
	COVERAGE_FILE=.coverage.unit coverage run --source=./awstaga -m unittest discover -s tests
	coverage combine
	coverage report
	coverage html

################################################################################
# Package targets
################################################################################

install: package
	pip3 install dist/awstaga-`yq -r .version conf/info.yaml | sed "s/-/_/g"`-py3-none-any.whl

reinstall:
	pip3 uninstall awstaga -y || echo "Nothing to uninstall..."
	make clean deps package install

package:
	python3 setup.py sdist bdist_wheel

publish:
	# TODO: publish to pypi

.PHONY: ci clean stage deps doc release lint complexity test test-integration coverage install reinstall package publish
