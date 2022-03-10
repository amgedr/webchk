import pytest

from webchk.utils import (
    read_input_file, get_parser, urls_from_xml, format_headers
)


def test_read_input_file():
    urls = read_input_file('test/urls.txt')
    urls_list = [
        'https://httpstat.us:443/200',
        'https://httpstat.us/200',
        'httpstat.us/301',
        'http://httpstat.us:80/302',
        'http://httpbin.org/status/200',
        'http://httpbin.org/status/404',
        'http://httpbin.org/relative-redirect/6',
        'http://httpbin.org/absolute-redirect/6',
    ]
    assert urls == urls_list


def test_command_parser_program_name():
    parser = get_parser()
    assert parser.prog == 'webchk'


def test_parse_xml_data():
    with open('test/sitemap.xml') as sitemap:
        xml = sitemap.read()

    urls_list = [
        'https://httpstat.us:443/200',
        'https://httpstat.us/200',
        'http://httpstat.us:80/302',
        'http://httpbin.org/status/200',
        'http://httpbin.org/status/404',
        'http://httpbin.org/relative-redirect/6',
        'http://httpbin.org/absolute-redirect/6',
    ]
    urls = urls_from_xml(xml)
    assert urls == urls_list


def test_valid_header_formats():
    cases = {
        ' Connection: keep-alive\n Content-Length: 5386':
        {
            'Connection': 'keep-alive',
            'Content-Length': '5386',
        },
        ' Cache-Control: no-cache\n Content-Type: text/html':
        {
            'Cache-Control': 'no-cache',
            'Content-Type': 'text/html',
        }
    }

    for expected, case in cases.items():
        assert format_headers(case) == expected


def test_invalid_header_formats():
    cases = [[], 123, 'abc']

    for case in cases:
        with pytest.raises(ValueError):
            format_headers(case)
