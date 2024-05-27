#!/usr/bin/env bash

set -euo pipefail

ROOT=$(git rev-parse --show-toplevel)
ROOTS=$(pants roots --roots-sep=' ')
RESOLVE=${1:-python-default}

# Remove old resolves symlinks
rm -rf ${ROOT}/dist/export/python/virtualenvs/$RESOLVE/*
# pants generate-lockfiles --resolve=$RESOLVE
pants export --resolve=$RESOLVE

PYTHON_VENV=$(find "$ROOT/dist/export/python/virtualenvs/$RESOLVE/" -mindepth 1 -maxdepth 1)
PYTHON_VERSION=$(basename "$PYTHON_VENV")
BIN="$RESOLVE/$PYTHON_VERSION/bin"

python -c "print('PYTHONPATH=\"./' + ':./'.join(\"${ROOTS}\".split()) + ':\$PYTHONPATH\"')" > ${ROOT}/.env

# Using typeCheckingMode=basic as I've found typing incompatibilities with mypy
settings=$(cat <<EOF
{
  "[python]": {
    "editor.formatOnSave": true,
    "editor.formatOnSaveMode": "file",
    "editor.codeActionsOnSave": {
      "source.fixAll": true
    },
  },
  "black-formatter.path": [
    "./dist/export/python/virtualenvs/$BIN/black"
  ],
  "mypy-type-checker.path": [
    "./dist/export/python/virtualenvs/$BIN/mypy"
  ],
  "python.envFile": "\${workspaceFolder}/.env",
  "python.testing.pytestEnabled": true,
  "python.terminal.activateEnvironment": true,
  "python.defaultInterpreterPath": "\${workspaceFolder}/dist/export/python/virtualenvs/$BIN/python",
  "python.testing.pytestPath": "\${workspaceFolder}/dist/export/python/virtualenvs/$BIN/pytest",
  "ruff.interpreter": [
    "./dist/export/python/virtualenvs/$BIN/python"
  ],
  "ruff.lint.args": [
    "--config=./pyproject.toml"
  ],
  "ruff.path": [
    "./dist/export/python/virtualenvs/$BIN/ruff"
  ],
}
EOF
)

if [ ! -f "$ROOT/.vscode/settings.json" ]; then
  mkdir -p "$ROOT/.vscode"
  touch "$ROOT/.vscode/settings.json"
fi
echo "$settings" | tee "$ROOT/.vscode/settings.json"
echo ""
echo "Run: >Python: Clear cache and reload window"
echo "in VSCode to pick up the new environment changes"
