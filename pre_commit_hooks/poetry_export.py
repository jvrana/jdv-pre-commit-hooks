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


def filehash(fname: str) -> str:
    return hashlib.md5(open(fname,'rb').read()).hexdigest()


def checksum(fname: str) -> bool:
    newchecksum = filehash(fname)
    oldchecksum = open(fname + ".checksum", 'r').read()
    return newchecksum == oldchecksum


def get_filehash_name(fname: str):
    return '.' + fname + '.checksum'


def save_filehash(fname: str):
    with open(get_filehash_name(fname), 'w') as f:
        f.write(filehash(fname))


def get_filehash(fname: str):
    with open(get_filehash_name(fname), 'r') as f:
        f.read(f)


def poetry_export():
    out = cmd_output('poetry', 'export', '-f', 'requirements.txt')
    with open('requirements.txt', 'w') as f:
        f.write(out)
    save_filehash('requirements.txt')


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.',
    )
    args = parser.parse_args(argv)

    retv = 0
    if 'pyproject.toml' in args.filenames or not os.path.isfile(get_filehash_name('requirements.txt')):
        poetry_export()
        retv = 1
    return retv


if __name__ == '__main__':
    exit(main())
