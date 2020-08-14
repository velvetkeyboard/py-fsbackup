.PHONY: build

company=velvetkeyboard
project=fsbackup
src_folder=fsbackup/

# [Virtualenv Bins]
# ------------------------------------------------------------------------------
venv=env
pip=$(venv)/bin/pip
python=$(venv)/bin/python
linter=$(venv)/bin/flake8

# [Semver]
# ------------------------------------------------------------------------------
git_version=$(shell git describe --tags)
app_version=$(shell $(python) -m fsbackup.cli -v)
wheel_package=$(project)-$(app_version)-py3-none-any.whl

pypi=test

ifeq ($(pypi),production)
	pypi_url=https://upload.pypi.org/legacy/
endif
ifeq ($(pypi), test)
	pypi_url=https://test.pypi.org/legacy/
endif

lint:
	@$(linter) $(src_folder)

build_wheel: lint
	$(python) setup.py bdist_wheel

publish_pypi: build_wheel
	twine upload \
		--repository-url $(pypi_url) \
		dist/$(wheel_package)
