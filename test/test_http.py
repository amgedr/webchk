import unittest

from webchk.http import http_response, parse_url


class Http(unittest.TestCase):
    def setUp(self):
        self.urls = {
            'https://httpstat.us:443/200': (200, 'httpstat.us:443'),
            'https://httpstat.us/200': (200, 'httpstat.us'),
            'httpstat.us/301': (301, 'httpstat.us'),
            'http://httpstat.us:80/302': (302, 'httpstat.us:80'),
            'https://codehill.com': (200, 'codehill.com'),
            'codehill.com': (301, 'codehill.com'),
            'http://httpbin.org/': (200, 'httpbin.org'),
            'http://httpbin.org/status/200': (200, 'httpbin.org'),
            'http://httpbin.org/status/404': (404, 'httpbin.org'),
        }

    def test_parse_url(self):
        for url, result in self.urls.items():
            loc = parse_url(url).netloc
            self.assertEqual(loc, result[1])

    def test_http_response(self):
        for url, result in self.urls.items():
            resp_code = http_response(url).status
            self.assertEqual(resp_code, result[0], url)

    def test_redirect_follows(self):
        url = 'https://httpstat.us/307'
        resp = http_response(url)
        total = 0
        while resp.redirect:
            fmt = '{} ... {} {} ({})'.format(
                resp.url, resp.status, resp.desc, resp.latency)
            self.assertEqual(str(resp), fmt)
            total += 1
            resp = resp.redirect
        self.assertEqual(total, 1)

    def test_unresolvable_domains(self):
        resp = http_response('http://!.c')
        self.assertEqual(str(resp), 'http://!.c ... Could not resolve')
