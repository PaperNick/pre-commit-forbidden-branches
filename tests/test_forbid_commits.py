import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from pre_commit_hook.forbid_commits import (
    get_project_root,
    get_git_dir,
    get_current_branch,
    is_merge_in_progress,
    is_commit_allowed,
    main,
    success_code,
    error_code,
)


class TestGetProjectRoot:
    def test_should_correctly_parse_the_path(self, monkeypatch):
        def mock_command_output(*args, **kwargs):
            return b"/path/to/my-project\n"

        monkeypatch.setattr(subprocess, "check_output", mock_command_output)

        path = get_project_root()
        assert path == Path("/path/to/my-project")


class TestGetGitDir:
    def test_should_correctly_return_git_folder_name_from_env_variable(self, monkeypatch):
        monkeypatch.setenv("GIT_DIR", "custom-git-dir-name")
        git_dir = get_git_dir()
        assert git_dir == Path("custom-git-dir-name")

    def test_should_return_the_default_git_folder_name_when_env_variable_is_not_set(self, monkeypatch):
        monkeypatch.delenv("GIT_DIR", raising=False)
        git_dir = get_git_dir()
        assert git_dir == Path(".git")


class TestGetCurrentBranch:
    def test_should_correctly_parse_the_current_branch_name(self, monkeypatch):
        def mock_command_output(*args, **kwargs):
            return b"test-branch-name\n"

        monkeypatch.setattr(subprocess, "check_output", mock_command_output)

        branch_name = get_current_branch()
        assert isinstance(branch_name, str)
        assert branch_name == "test-branch-name"

    def test_should_return_empty_string_when_subprocess_exception_is_raised(self, monkeypatch):
        def mock_command_output(*args, **kwargs):
            raise subprocess.CalledProcessError(128, ["some-command"])

        monkeypatch.setattr(subprocess, "check_output", mock_command_output)

        branch_name = get_current_branch()
        assert branch_name == ""


class TestIsMergeInProgress:
    def test_should_return_false_when_merge_head_file_does_not_exist(self, tmp_path):
        assert is_merge_in_progress(git_dir_absolute=tmp_path) is False

    def test_should_return_true_when_merge_head_file_exists(self, tmp_path):
        merge_head = tmp_path / Path("MERGE_HEAD")
        merge_head.write_text("some-sha-value")
        assert is_merge_in_progress(git_dir_absolute=tmp_path) is True


class TestIsCommitAllowed:
    @patch("pre_commit_hook.forbid_commits.is_merge_in_progress")
    def test_should_not_allow_commit_if_branch_name_is_in_forbidden_list(
        self,
        mock_is_merge_in_progress,
    ):
        mock_is_merge_in_progress.return_value = False

        branch_name = "my-branch"
        forbidden_branches = ["my-branch"]
        assert is_commit_allowed(branch_name, forbidden_branches) is False

    @patch("pre_commit_hook.forbid_commits.is_merge_in_progress")
    def test_should_allow_commit_if_branch_name_is_not_in_forbidden_list(
        self,
        mock_is_merge_in_progress,
    ):
        mock_is_merge_in_progress.return_value = False

        branch_name = "allowed-branch"
        forbidden_branches = ["forbidden-branch"]
        assert is_commit_allowed(branch_name, forbidden_branches) is True

    @patch("pre_commit_hook.forbid_commits.is_merge_in_progress")
    def test_should_always_allow_commit_if_there_is_merge_in_progress(
        self,
        mock_is_merge_in_progress,
    ):
        mock_is_merge_in_progress.return_value = True

        branch_name = "forbidden"
        forbidden_branches = ["forbidden"]
        assert is_commit_allowed(branch_name, forbidden_branches) is True


class TestMain:
    @patch("pre_commit_hook.forbid_commits.is_commit_allowed")
    @patch("pre_commit_hook.forbid_commits.get_current_branch")
    def test_should_return_error_code_when_commiting_is_not_allowed(
        self,
        mock_get_current_branch,
        mock_is_commit_allowed,
    ):
        mock_get_current_branch.return_value = "some-branch"
        mock_is_commit_allowed.return_value = False
        assert main(["master"]) == error_code

    @patch("pre_commit_hook.forbid_commits.is_commit_allowed")
    @patch("pre_commit_hook.forbid_commits.get_current_branch")
    def test_should_return_success_code_when_commiting_is_allowed(
        self,
        mock_get_current_branch,
        mock_is_commit_allowed,
    ):
        mock_get_current_branch.return_value = "some-branch"
        mock_is_commit_allowed.return_value = True
        assert main(["master"]) == success_code
