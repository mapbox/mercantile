#!/bin/bash
(
    python -m pip install pip-tools &> /dev/null &&
    pip-compile -o requirements.txt.new --allow-unsafe --strip-extras --generate-hashes requirements.in &&
    mv requirements.txt.new requirements.txt &&
    python -m pip install -r requirements.txt
)
