from pre_commit_hooks.poetry_export import main, cmd_output


def test_adding_nothing(temp_dir):
    with temp_dir.as_cwd():
        # Should not fail with default
        temp_dir.join('f.py').write('a' * 10000)
        cmd_output('git', 'add', 'f.py')
        assert main(argv=['f.py']) == 0


def test_adding_pyproject(temp_dir):
    with temp_dir.as_cwd():
        # Should not fail with default
        cmd_output('git', 'add', 'pyproject.toml')
        assert main(argv=['pyproject.toml']) == 1


def test_adding_requirements(temp_dir):
    with temp_dir.as_cwd():
        # Should not fail with default
        f = 'requirements.txt'
        temp_dir.join(f).write('a' * 1000)
        cmd_output('git', 'add', f)
        assert main(argv=[f]) == 1


def test_adding_lock(temp_dir):
    with temp_dir.as_cwd():
        # Should not fail with default
        f = 'poetry.lock'
        cmd_output('git', 'add', f)
        assert main(argv=[f]) == 1


def test_adding_requirements_twice(temp_dir):
    with temp_dir.as_cwd():
        # Should not fail with default
        f = 'requirements.txt'
        temp_dir.join(f).write('a' * 1000)
        cmd_output('git', 'add', f)
        assert main(argv=[f]) == 1
        cmd_output('git', 'add', f)
        assert main(argv=[f]) == 0
