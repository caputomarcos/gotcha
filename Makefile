.ONESHELL:
ENV_PREFIX=$(shell python -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")
USING_POETRY=$(shell grep "tool.poetry" pyproject.toml && echo "yes")

.SILENT: clean

NAME            := gotcha
SRC             := gotcha
ENTRYPOINT      := $(SRC)/__init__.py
DIST            := dist
COMPILED        := $(DIST)/$(NAME)
STATIC_COMPILED := $(COMPILED).static


.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: show
show:             ## Show the current environment.
	@echo "Current environment:"
	@if [ "$(USING_POETRY)" ]; then poetry env info && exit; fi
	@echo "Running using $(ENV_PREFIX)"
	@$(ENV_PREFIX)python -V
	@$(ENV_PREFIX)python -m site

.PHONY: deps
deps:
	@requires=$(shell mktemp)
	@python setup.py -q dependencies > \$requires &> /dev/null
	@pip install -r \$requires &> /dev/null
	@rm \$requires

.PHONY: dev-deps
dev-deps:
	@pip install -r requirements-dev.txt &> /dev/null

.PHONY: fmt
fmt: dev-deps     ## Format code using black & isort.
	$(ENV_PREFIX)isort $(NAME)/
	$(ENV_PREFIX)black -l 79  --target-version=py310 $(NAME)/
	$(ENV_PREFIX)black -l 79  --target-version=py310 tests/

.PHONY: lint
lint:
	black .
	flake8

.PHONY: lint-check
lint-check:
	flake8
	black --check --diff .

.PHONY: test
test:
	python -m pytest

.PHONY: build
build:            ## Build GOTCHA.
	python setup.py sdist bdist_wheel

.PHONY: pyinstaller
pyinstaller: deps
	python setup.py pyinstaller

.PHONY: staticx_deps
staticx_deps:
	command -v patchelf > /dev/null 2>&1 || (echo "patchelf is not available. install it in order to use staticx" && false)

.PHONY: pyinstaller_static
pyinstaller_static: staticx_deps pyinstaller
	staticx $(COMPILED) $(STATIC_COMPILED)

.PHONY: install
install:          ## Install GOTCHA in dev mode.
	pip install .

.PHONY: uninstall
uninstall:        ## Uninstall GOTCHA in dev mode.
	pip uninstall $(NAME)

.PHONY: publish
publish:          ## PYPI Publish. 
	twine upload dist/*

.PHONY: clean
clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .eggs
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build

