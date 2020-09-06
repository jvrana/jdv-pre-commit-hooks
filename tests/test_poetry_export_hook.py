from poetry_export_hook.poetry_export import cmd_output
from poetry_export_hook.poetry_export import main
from poetry_export_hook.poetry_export import parse_args
from poetry_export_hook.poetry_export import poetry_cmd


def pytest_addoption(parser):
    parser.addoption(
        "--log", action="store", default="WARNING", help="set logging level"
    )


class TestParseArgs:
    def test_parse_args_default(self):
        args = parse_args(argv=["f1", "f2"])
        assert args.filenames == ["f1", "f2"]
        assert args.requirements == "requirements.txt"
        assert args.verbose == 0
        assert args.dev is False
        assert args.extras == []

    def test_parse_args_requirements(self):
        args = parse_args(argv=["f1", "f2", "--requirements", "r.txt"])
        assert args.filenames == ["f1", "f2"]
        assert args.requirements == "r.txt"
        assert args.verbose == 0
        assert args.dev is False
        assert args.extras == []

    def test_parse_args_v(self):
        args = parse_args(argv=["f1", "f2", "-v"])
        assert args.filenames == ["f1", "f2"]
        assert args.requirements == "requirements.txt"
        assert args.verbose == 1
        assert args.dev is False
        assert args.extras == []

    def test_parse_args_vv(self):
        args = parse_args(argv=["f1", "f2", "-vv"])
        assert args.filenames == ["f1", "f2"]
        assert args.requirements == "requirements.txt"
        assert args.verbose == 2
        assert args.dev is False
        assert args.extras == []

    def test_parse_args_vvv(self):
        args = parse_args(argv=["f1", "f2", "-vvv"])
        assert args.filenames == ["f1", "f2"]
        assert args.requirements == "requirements.txt"
        assert args.verbose == 3
        assert args.dev is False
        assert args.extras == []

    def test_parse_args_dev(self):
        args = parse_args(argv=["f1", "f2", "-D"])
        assert args.filenames == ["f1", "f2"]
        assert args.requirements == "requirements.txt"
        assert args.verbose == 0
        assert args.dev is True
        assert args.extras == []

    def test_parse_args_extras1(self):
        args = parse_args(argv=["f1", "f2", "-E", "docs"])
        assert args.filenames == ["f1", "f2"]
        assert args.requirements == "requirements.txt"
        assert args.verbose == 0
        assert args.dev is False
        assert args.extras == ["docs"]

    def test_parse_args_extras2(self):
        args = parse_args(argv=["f1", "f2", "-E", "docs", "-E", "lint"])
        assert args.filenames == ["f1", "f2"]
        assert args.requirements == "requirements.txt"
        assert args.verbose == 0
        assert args.dev is False
        assert args.extras == ["docs", "lint"]


def test_poetry_cmd():
    out = poetry_cmd("requirements-dev.txt", True, ("docs", "linter"))
    expected = "poetry export -f requirements.txt --dev -E docs -E linter".split()
    o = " ".join(out)
    e = " ".join(expected)
    print(o)
    print(e)
    assert o == e


def test_adding_nothing(temp_dir):
    with temp_dir.as_cwd():
        # Should not fail with default
        temp_dir.join("f.py").write("a" * 10000)
        cmd_output("git", "add", "f.py")
        assert main(argv=["f.py"]) == 0


def test_adding_pyproject(temp_dir):
    with temp_dir.as_cwd():
        # Should not fail with default
        cmd_output("git", "add", "pyproject.toml")
        assert main(argv=["pyproject.toml"]) == 1


def test_adding_requirements(temp_dir):
    with temp_dir.as_cwd():
        # Should not fail with default
        f = "requirements.txt"
        temp_dir.join(f).write("a" * 1000)
        cmd_output("git", "add", f)
        assert main(argv=[f]) == 1


def test_adding_lock(temp_dir):
    with temp_dir.as_cwd():
        # Should not fail with default
        f = "poetry.lock"
        cmd_output("git", "add", f)
        assert main(argv=[f]) == 1


def test_adding_requirements_twice(temp_dir):
    with temp_dir.as_cwd():
        # Should not fail with default
        f = "requirements.txt"
        temp_dir.join(f).write("a" * 1000)
        cmd_output("git", "add", f)
        assert main(argv=[f]) == 1
        cmd_output("git", "add", f)
        assert main(argv=[f]) == 0


def test_new_reqs_file_not_added(temp_dir):
    with temp_dir.as_cwd():
        # Should not fail since 'requirements-dev.txt' is not added to git yet
        f = "requirements.txt"
        temp_dir.join(f).write("a" * 1000)
        cmd_output("git", "add", f)
        assert main(argv=[f, "--requirements", "requirements-dev.txt"]) == 0


def test_new_reqs_file_added(temp_dir):
    with temp_dir.as_cwd():
        # Should fail since 'requirements-dev.txt' is added to git
        f = "requirements-dev.txt"
        temp_dir.join(f).write("a" * 1000)
        cmd_output("git", "add", f)
        assert main(argv=[f, "--requirements", f]) == 1
