import argparse
import os
import subprocess
import sys
from pathlib import Path


success_code = 0
error_code = 1


def get_project_root() -> Path:
    # TODO: Test on windows
    project_dir = subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
    return Path(project_dir.decode(sys.stdout.encoding).strip())


def get_git_dir() -> Path:
    return Path(os.environ.get("GIT_DIR", ".git"))


def get_current_branch() -> str:
    try:
        branch_name = subprocess.check_output(
            ["git", "symbolic-ref", "--quiet", "--short", "HEAD"]
        )
    except subprocess.CalledProcessError:
        # This command will return a non-zero
        # exit status code if HEAD is detached
        return ""
    return branch_name.decode(sys.stdout.encoding).strip()


def is_merge_in_progress(project_dir: Path = None, git_dir: Path = None) -> bool:
    """
    Determine whether a git merge is in progress.
    """
    if project_dir is None:
        project_dir = get_project_root()

    if git_dir is None:
        git_dir = get_git_dir()

    merge_head = project_dir / git_dir / Path("MERGE_HEAD")
    return merge_head.is_file()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [branches]",
        description="Prevent commits in the specified branches",
        allow_abbrev=False,
    )
    parser.add_argument("forbidden_branches", type=str, nargs="*", default=[])
    args = parser.parse_args(argv)

    branch_name = get_current_branch()
    if branch_name in args.forbidden_branches:
        if is_merge_in_progress():
            # Do not interrupt the merge in progress
            return success_code

        print("You are not allowed to commit in this branch.")
        return error_code

    return success_code


if __name__ == "__main__":
    exit(main())
