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

from pre_commit_hooks.poetry_export import poetry_export


def test_adding_something(temp_git_dir):
    with temp_git_dir.as_cwd():
        temp_git_dir.join("pyproject.toml").write(pyprojecttoml)
        poetry_export()