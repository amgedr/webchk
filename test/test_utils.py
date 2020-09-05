import unittest

from webchk.utils import read_input_file, get_parser, urls_from_xml


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
