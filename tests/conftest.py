import shutil
from os.path import abspath
from os.path import dirname
from os.path import join

import pytest

from poetry_export_hook.poetry_export import cmd_output
from poetry_export_hook.poetry_export import logger

logger.setLevel("DEBUG")
here = dirname(abspath(__file__))


@pytest.fixture
def fixtures():
    return join(here, "fixtures")


@pytest.fixture
def temp_git_dir(tmpdir):
    git_dir = tmpdir.join("gits")
    cmd_output("git", "init", "--", str(git_dir))
    yield git_dir


@pytest.fixture
def temp_dir(temp_git_dir):
    shutil.copy(
        join(here, "fixtures", "pyproject.toml"),
        temp_git_dir.join("pyproject.toml"),
    )
    shutil.copy(
        join(here, "fixtures", "poetry.lock"),
        temp_git_dir.join("poetry.lock"),
    )
    return temp_git_dir
