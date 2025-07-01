#!/bin/bash
cd /home/kavia/workspace/code-generation/minimal-tic-tac-toe-97952-d32c8ea6/tic_tac_toe_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

