import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List


success_code = 0
error_code = 1


def get_project_root() -> Path:
    project_dir = subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
    return Path(project_dir.decode(sys.stdout.encoding).strip())


def get_git_dir() -> Path:
    return Path(os.environ.get("GIT_DIR", ".git"))


def get_current_branch() -> str:
    try:
        branch_name: bytes = subprocess.check_output(
            ["git", "symbolic-ref", "--quiet", "--short", "HEAD"]
        )
    except subprocess.CalledProcessError:
        # This command will return a non-zero
        # exit status code if HEAD is detached
        return ""
    return branch_name.decode(sys.stdout.encoding).strip()


def is_merge_in_progress(git_dir_absolute: Path = None) -> bool:
    if git_dir_absolute is None:
        git_dir_absolute = get_project_root() / get_git_dir()

    merge_head = git_dir_absolute / Path("MERGE_HEAD")
    return merge_head.is_file()


def is_commit_allowed(branch_name: str, forbidden_branches: List[str]) -> bool:
    if is_merge_in_progress():
        # Do not interrupt the merge in progress
        return True

    if branch_name in forbidden_branches:
        return False

    return True


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [branches]",
        description="Prevent commits in the specified branches",
        allow_abbrev=False,
    )
    parser.add_argument("forbidden_branches", type=str, nargs="*", default=[])
    args = parser.parse_args(argv)

    if not is_commit_allowed(get_current_branch(), args.forbidden_branches):
        print("You are not allowed to commit in this branch.")
        return error_code

    return success_code


if __name__ == "__main__":
    exit(main())
