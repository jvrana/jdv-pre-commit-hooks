import argparse
from typing import Sequence
import hashlib
import subprocess
from typing import Any
from typing import Optional
import os


class CalledProcessError(RuntimeError):
    pass


def cmd_output(*cmd: str, retcode: Optional[int] = 0, **kwargs: Any) -> str:
    kwargs.setdefault('stdout', subprocess.PIPE)
    kwargs.setdefault('stderr', subprocess.PIPE)
    proc = subprocess.Popen(cmd, **kwargs)
    stdout, stderr = proc.communicate()
    stdout = stdout.decode()
    if retcode is not None and proc.returncode != retcode:
        raise CalledProcessError(cmd, retcode, proc.returncode, stdout, stderr)
    return stdout


def compare(r1):
    if not os.path.isfile('requirements.txt'):
        return False
    with open('requirements.txt', 'r') as f:
        r2 = f.read()
    return r1.strip() == r2.strip()


def poetry_export():
    retv = 0
    out = cmd_output('poetry', 'export', '-f', 'requirements.txt')
    print(os.path.isfile('requirements.txt'))
    if not os.path.isfile('requirements.txt') or open('requirements.txt', 'r').read().strip() != out.strip():
        with open('requirements.txt', 'w') as f:
            f.write(out)
        retv = 1
    return retv


PYPROJECT = "pyproject.toml"
POETRYLOCK = "poetry.lock"
REQUIREMENTS = "requirements.txt"

def run(filenames):
    retv = 0
    print(filenames)
    if {PYPROJECT, POETRYLOCK, REQUIREMENTS}.intersection(set(filenames)):
        retv = poetry_export()
    else:
        print("skipping")
    return retv


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.',
    )
    args = parser.parse_args(argv)
    return run(args.filenames)


if __name__ == '__main__':
    exit(main())
