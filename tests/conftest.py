import pytest

from pre_commit_hooks.util import cmd_output

pyprojecttoml = """
[tool.poetry]
name = "jdv-pre-commit-hooks"
version = "0.1.0"
description = ""
authors = ["Justin Vrana <justin.vrana@gmail.com>"]

[tool.poetry.dependencies]
python = "^3.7"


[tool.poetry.dev-dependencies]

[build-system]
requires = ["poetry>=0.12"]
build-backend = "poetry.masonry.api"
""".strip()

from os.path import isfile, abspath, dirname, join
import shutil

here = dirname(abspath(__file__))


@pytest.fixture
def fixtures():
    return join(here, 'fixtures')


@pytest.fixture
def temp_git_dir(tmpdir):
    git_dir = tmpdir.join('gits')
    cmd_output('git', 'init', '--', str(git_dir))
    yield git_dir


@pytest.fixture
def temp_dir(temp_git_dir):
    shutil.copy(join(here, 'fixtures', 'pyproject.toml'), temp_git_dir.join('pyproject.toml'), )
    shutil.copy(join(here, 'fixtures', 'poetry.lock'), temp_git_dir.join('poetry.lock'), )
    return temp_git_dir

