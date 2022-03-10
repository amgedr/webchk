import pytest

from webchk.http import http_response, parse_url, HTTPRequests

TIMEOUT = 3


@pytest.fixture
def urls_list():
    return {
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


def test_parse_url(urls_list):
    for url, result in urls_list.items():
        loc = parse_url(url).netloc
        assert loc == result[1]


def test_http_response(urls_list):
    for url, result in urls_list.items():
        req = HTTPRequests(url, timeout=TIMEOUT)
        resp_code = http_response(url, req).status
        assert resp_code == result[0], url


def test_redirect_follows():
    url = 'https://httpstat.us/307'

    req = HTTPRequests(url, timeout=TIMEOUT)
    resp = http_response(url, req)
    total = 0
    while resp.redirect:
        fmt = '{} ... {} {} ({})'.format(
            resp.url, resp.status, resp.desc, resp.latency)
        assert str(resp) == fmt
        total += 1
        resp = resp.redirect
        assert total == 1


def test_unresolvable_domains():
    req = HTTPRequests(None, timeout=TIMEOUT)
    resp = http_response('http://!.c', req)
    assert str(resp) == 'http://!.c ... Could not resolve'


def test_timeouts():
    url = 'http://httpbin.org/delay/5'
    req = HTTPRequests(url, timeout=1)
    resp = http_response(url, req)
    assert resp.desc == 'Operation timed out'
