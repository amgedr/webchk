import unittest

from webchk.utils import (
    read_input_file, get_parser, urls_from_xml, format_headers
)


class FileIOTest(unittest.TestCase):
    def setUp(self):
        self.urls = read_input_file('test/urls.txt')

    def test_read_input_file(self):
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
        self.assertEqual(self.urls, urls_list)


class CommandParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = get_parser()

    def test_strings(self):
        self.assertEqual(self.parser.prog, 'webchk')


class XmlParserTest(unittest.TestCase):
    def setUp(self):
        with open('test/sitemap.xml') as sitemap:
            self.xml = sitemap.read()

    def test_parse_xml_data(self):
        urls_list = [
            'https://httpstat.us:443/200',
            'https://httpstat.us/200',
            'http://httpstat.us:80/302',
            'http://httpbin.org/status/200',
            'http://httpbin.org/status/404',
            'http://httpbin.org/relative-redirect/6',
            'http://httpbin.org/absolute-redirect/6',
        ]
        urls = urls_from_xml(self.xml)
        self.assertEqual(urls, urls_list)


class HeadersFormatterTest(unittest.TestCase):
    def test_valid_headers(self):
        cases = {
            'Connection: keep-alive\nContent-Length: 5386':
            {
                'Connection': 'keep-alive',
                'Content-Length': '5386',
            },
            'Cache-Control: no-cache\nContent-Type: text/html':
            {
                'Cache-Control': 'no-cache',
                'Content-Type': 'text/html',
            }
        }

        for expected, case in cases.items():
            self.assertEqual(format_headers(case), expected)

    def test_invalid_value(self):
        cases = [[], 123, 'abc']

        for case in cases:
            with self.assertRaises(ValueError):
                format_headers(case)
