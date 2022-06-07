import logging

url = 'http://0.0.0.0:8000'
headers = {
    'User-Agent': 'test',
}


logging.basicConfig(level='INFO')
logger = logging.getLogger('test')


def mock_true():
    return True

