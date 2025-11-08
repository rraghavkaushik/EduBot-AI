#!/bin/bash
# Wrapper script for mutation testing that sets up the environment correctly
cd "$(dirname "$0")"
export PYTHONPATH="$(pwd):$PYTHONPATH"
pytest "$@"

