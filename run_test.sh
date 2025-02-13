#!/bin/bash

set -e

: "${AIRFLOW__CORE__FERNET_KEY:=${FERNET_KEY:=$(python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)")}}"
export AIRFLOW__CORE__FERNET_KEY

# avoid issues with .pyc/pyo files when mounting source directory
export PYTHONOPTIMIZE=

echo "running pylint"
PYLINTHOME=/tmp/datahub-dags-pylint \
 pylint tests/ data_science_pipeline/ dags/

echo "running flake8"
flake8 tests/ data_science_pipeline/ dags/

pytest tests/ -p no:cacheprovider -s --disable-warnings

echo "done"
