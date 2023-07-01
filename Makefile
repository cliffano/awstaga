version=`yq -r .version conf/info.yaml`

ci: clean deps lint test coverage complexity doc package reinstall test-integration

# Exclude complexity due to complexity requiring no uncommited local change
dev: clean deps lint test coverage doc package reinstall test-integration

clean:
	rm -rf stage *.egg-info build dist docs/ awstaga/_pycache_/ awstaga/*.pyc tests/_pycache_/ tests/*.pyc .coverage

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
release-major:
	sed -i -e 's/rc0/-rc0/' conf/info.yaml
	rtk release --release-increment-type major
	sed -i -e 's/-rc0.0/rc0/' conf/info.yaml
	git commit conf/info.yaml -m "Switch version to Python setuptools versioning scheme"

release-minor:
	sed -i -e 's/rc0/-rc0/' conf/info.yaml
	rtk release --release-increment-type minor
	sed -i -e 's/-rc0.0/rc0/' conf/info.yaml
	git commit conf/info.yaml -m "Switch version to Python setuptools versioning scheme"

release-patch:
	sed -i -e 's/rc0/-rc0/' conf/info.yaml
	rtk release --release-increment-type patch
	sed -i -e 's/-rc0.0/rc0/' conf/info.yaml
	git commit conf/info.yaml -m "Switch version to Python setuptools versioning scheme"

lint: stage
	mkdir -p stage/lint/pylint/ docs/lint/pylint/
	pylint awstaga/*.py awstaga/loaders/*.py tests/*.py tests/loaders/*.py tests-integration/*.py examples/*.py
	pylint awstaga/*.py awstaga/loaders/*.py tests/*.py tests/loaders/*.py tests-integration/*.py examples/*.py --output-format=pylint_report.CustomJsonReporter > stage/lint/pylint/report.json
	pylint_report stage/lint/pylint/report.json -o docs/lint/pylint/index.html

complexity: stage
	wily build awstaga/
	wily report docs/complexity/wily/index.html

test:
	pytest -v tests --html=docs/test/pytest/index.html --self-contained-html

test-integration:
	rm -rf stage/test-integration/ && mkdir -p stage/test-integration/
	python3 -m unittest tests-integration/*.py
	cd examples/ && python3 log.py

coverage:
	COVERAGE_FILE=.coverage.unit coverage run --source=./awstaga -m unittest discover -s tests
	coverage combine
	coverage report
	coverage html

install: package
	pip3 install dist/awstaga-`yq -r .version conf/info.yaml | sed "s/-/_/g"`-py3-none-any.whl

uninstall:
	pip3 uninstall awstaga -y

reinstall:
	make uninstall || echo "Nothing to uninstall..."
	make clean deps package install

package:
	python3 setup.py sdist bdist_wheel

publish:
	twine upload dist/*

.PHONY: ci dev clean stage deps deps-extra doc release lint complexity test test-integration coverage install uninstall reinstall package publish
