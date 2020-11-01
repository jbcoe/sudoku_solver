#!/bin/bash

readonly DIR=$(cd "$(dirname "$0")"; pwd)
readonly PYENV="${DIR}/__pyenv__"

if [ ${1:-" "} == "clean" ]; then
    (   
        echo Removing existing PyEnv at "${PYENV}"
        rm -rf "${PYENV}"
    )
fi

if [ ! -d "${PYENV}" ]; then
    echo Creating a fresh PyEnv at "${PYENV}"
    python -m venv "${PYENV}"
    ${PYENV}/bin/pip install --upgrade -r requirements.txt; 
fi

source "${PYENV}/bin/activate"
python -m pytest -n auto -v "${DIR}/tests"
