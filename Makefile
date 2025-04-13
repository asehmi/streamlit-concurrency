PYTHON_BIN ?= python3
CONDA_ENV ?= streamlit_dev_py310
CONDA_YML ?= conda-py310.yaml

run: deps
	venv/bin/streamlit run streamlit-concurrency.py --logger.level=INFO # --server.address=0.0.0.0

deps: venv/.deps_installed requirements.txt


venv/.deps_installed: requirements.txt
	venv/bin/pip install -r requirements.txt --editable .
	touch $@

test:
	venv/bin/pytest

format:
	venv/bin/ruff format .

venv: venv/.venv_created


# default: create venv with $PYTHON_BIN in $PATH
venv/.venv_created: Makefile
	$(PYTHON_BIN) -mvenv ./venv
	touch $@

# alt: create venv with conda python 
conda-venv: .conda_env_created
	micromamba run --attach '' -n $(CONDA_ENV) $(PYTHON_BIN) -mvenv ./venv
	touch venv/.venv_created

.conda_env_created: $(CONDA_YML)
	# setup conda environment AND env-wise deps
	micromamba env create -n $(CONDA_ENV) --yes -f $(CONDA_YML)
	touch $@

upgrade-deps:
	venv/bin/pur -r requirements.txt
