import os

from urllib import request


def read_input(day):
    url = f'https://adventofcode.com/2023/day/{day}/input'
    session = os.environ.get("AOC_SESSION")
    req = request.Request(url, headers={'Cookie':f'session={session}'})
    with request.urlopen(req) as f:
        for _line in f.readlines():
            yield _line.decode('utf-8').strip()
