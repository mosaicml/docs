# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= $(VENV_FOLDER)/bin/sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# virtualenv
VENV_FOLDER	  = .venv
PYTHON        = python3.10
REQUIREMENTS  = requirements.txt

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

build: docs

clean-py:
	# python artifacts
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf .cache dist build
	rm -rf .coverage .pytest_cache

clean-venv:
	# virtual environment
	rm -rf ${VENV_FOLDER}

clean: clean-py clean-venv

docs: clean-py venv
	rm -rf .cache dist build
	@. $(VENV_FOLDER)/bin/activate && \
	$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	cd $(BUILDDIR)/html && python3 -m http.server

venv:
	@if [ ! -d "$(VENV_FOLDER)" ]; then \
		echo "Creating virtual environment using $(PYTHON)..." && \
		$(PYTHON) -m venv $(VENV_FOLDER) && \
		echo "Installing requirements..." && \
		. $(VENV_FOLDER)/bin/activate && \
        pip install -r $(REQUIREMENTS); \
	else \
		echo "Virtual environment already exists at $(VENV_FOLDER)"; \
	fi


.PHONY: help Makefile clean-venv venv

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
