#!/bin/bash

readonly DIR=$(cd "$(dirname "$0")"; pwd)
readonly PYENV="${DIR}/__pyenv__"

if [ ${1:-" "} == "clean" ]; then
    (   
        echo Removing existing PyEnv at "${PYENV}"
        rm -rf "${PYENV}"
    )
fi

python -m venv "${PYENV}"
source "${PYENV}/bin/activate"
pip install --upgrade -r requirements.txt
python -m nose -v "${DIR}"
