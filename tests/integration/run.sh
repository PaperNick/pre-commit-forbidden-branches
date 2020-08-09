#!/bin/bash

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# Discover all tests scripts in the tests/integration folder and execute them
# Note: the test shell scripts need to have the executable flag set (chmod +x)
find "$SCRIPT_DIR" -type f -iname "test*.sh" | xargs -I{} bash -c '"{}"'
