import argparse
import os
import subprocess


success_code = 0
error_code = 1


def get_project_root_dir() -> str:
    # TODO: Test on windows
    project_dir = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    )
    return project_dir.strip()


def get_git_dir() -> str:
    return os.environ.get("GIT_DIR", ".git")


def get_current_branch() -> str:
    branch_name = subprocess.check_output(
        ["git", "symbolic-ref", "--short", "HEAD"], text=True
    )
    return branch_name.strip()


def is_merge_in_progress(project_dir="", git_dir="") -> bool:
    """
    Determine whether a git merge is in progress.
    """
    if not project_dir:
        project_dir = get_project_root_dir()

    if not git_dir:
        git_dir = get_git_dir()

    return os.path.isfile(os.path.join(project_dir, git_dir, "MERGE_HEAD"))


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
