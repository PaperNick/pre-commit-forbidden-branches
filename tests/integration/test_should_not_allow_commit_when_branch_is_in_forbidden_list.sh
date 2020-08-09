#!/bin/bash

SCRIPT_NAME=$(basename "$(readlink -f "$0")")
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
PROJECT_ROOT_DIR=$(dirname "$(dirname "$SCRIPT_DIR")")

TEST_PROJECT="test_project"
TEST_PROJECT_DIR="$SCRIPT_DIR/$TEST_PROJECT"
MAIN_BRANCH_NAME="master"


function cleanup () {
    rm -rf "$TEST_PROJECT_DIR"
}

trap cleanup EXIT

# Arrange
cleanup
mkdir "$TEST_PROJECT_DIR" || exit 1
cd "$TEST_PROJECT_DIR"
git init --quiet
git checkout --quiet -b "$MAIN_BRANCH_NAME"
cp -R "$PROJECT_ROOT_DIR/pre_commit_hook" "$TEST_PROJECT_DIR"

# Act
output_message=$(python "$TEST_PROJECT_DIR/pre_commit_hook/forbid_commits.py" "$MAIN_BRANCH_NAME")
output_exit_code=$?

# Assert
if [ "$output_message" = "You are not allowed to commit in this branch." ]; then
    echo "Test 1: PASS - $SCRIPT_NAME"
else
    echo "Test 1: FAIL - $SCRIPT_NAME"
    exit 1
fi

if [ "$output_exit_code" = "1" ]; then
    echo "Test 2: PASS - $SCRIPT_NAME"
else
    echo "Test 2: FAIL - $SCRIPT_NAME"
    exit 1
fi
