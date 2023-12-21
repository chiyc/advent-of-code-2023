import os

from urllib import request


def read_input(day, sample=True):
    url = f'https://adventofcode.com/2023/day/{day}/input'
    session = os.environ.get("AOC_SESSION")
    req = request.Request(url, headers={'Cookie':f'session={session}'})
    with request.urlopen(req) as f:
        for _line in f.readlines():
            yield _line.decode('utf-8').strip()


def sample_input(day):
    sample = []
    if day == 5:
        sample = [
            'seeds: 79 14 55 13',
            '',
            'seed-to-soil map:',
            '50 98 2',
            '52 50 48',
            '',
            'soil-to-fertilizer map:',
            '0 15 37',
            '37 52 2',
            '39 0 15',
            '',
            'fertilizer-to-water map:',
            '49 53 8',
            '0 11 42',
            '42 0 7',
            '57 7 4',
            '',
            'water-to-light map:',
            '88 18 7',
            '18 25 70',
            '',
            'light-to-temperature map:',
            '45 77 23',
            '81 45 19',
            '68 64 13',
            '',
            'temperature-to-humidity map:',
            '0 69 1',
            '1 0 69',
            '',
            'humidity-to-location map:',
            '60 56 37',
            '56 93 4',
        ]
    elif day == 19:
        sample = [
            'px{a<2006:qkq,m>2090:A,rfg}',
            'pv{a>1716:R,A}',
            'lnx{m>1548:A,A}',
            'rfg{s<537:gd,x>2440:R,A}',
            'qs{s>3448:A,lnx}',
            'qkq{x<1416:A,crn}',
            'crn{x>2662:A,R}',
            'in{s<1351:px,qqz}',
            'qqz{s>2770:qs,m<1801:hdj,R}',
            'gd{a>3333:R,R}',
            'hdj{m>838:A,pv}',
            '',
            '{x=787,m=2655,a=1222,s=2876}',
            '{x=1679,m=44,a=2067,s=496}',
            '{x=2036,m=264,a=79,s=2244}',
            '{x=2461,m=1339,a=466,s=291}',
            '{x=2127,m=1623,a=2188,s=1013}',
        ]
    elif day == 21:
        sample = [
            '...........',
            '.....###.#.',
            '.###.##..#.',
            '..#.#...#..',
            '....#.#....',
            '.##..S####.',
            '.##..#...#.',
            '.......##..',
            '.##.#.####.',
            '.##..##.##.',
            '...........',
        ]
    for line in sample:
        yield line
