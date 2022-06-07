import shlex
import subprocess

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(
    prefix='/test',
    tags=['test'],
)


def run_tests(filename: str = ''):
    command = f'pytest -o log_cli=true --log-cli-level=DEBUG test/{filename}'
    command_list = shlex.split(command)
    result = subprocess.run(command_list, capture_output=True)
    return result.stdout.decode()


@router.get('/', response_class=PlainTextResponse)
def test_all():
    return run_tests()


@router.get('/statistics/', response_class=PlainTextResponse)
def test_references():
    return run_tests('test_statistics.py')

