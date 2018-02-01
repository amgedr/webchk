import http.client
from urllib.parse import urlparse
import socket
import ssl
import timeit
from webchk.utils import urls_from_xml


class Result:
    """Holds result of an URL check.

    The redirect attribute is a Result object that the URL was redirected to.

    The sitemap_urls attribute will contain a list of Result object if url
    is a sitemap file and http_response() was run with parse set to True.
    """
    def __init__(self, url):
        self.url = url
        self.status = 0
        self.desc = ''
        self.headers = None
        self.latency = 0
        self.content = ''
        self.redirect = None
        self.sitemap_urls = None

    def __repr__(self):
        if self.status == 0:
            return '{} ... {}'.format(self.url, self.desc)
        return '{} ... {} {} ({})'.format(self.url, self.status, self.desc, self.latency)

    def fill_headers(self, headers):
        """Takes a list of tuples and convers it a dictionary."""
        self.headers = {h[0]: h[1] for h in headers}


def parse_url(url):
    """Returns an object with properties representing

    scheme:   URL scheme specifier
    netloc:   Network location part
    path:     Hierarchical path
    params:   Parameters for last path element
    query:    Query component
    fragment: Fragment identifier
    username: User name
    password: Password
    hostname: Host name (lower case)
    port:     Port number as integer, if present
    """
    loc = urlparse(url)

    # if the scheme (http, https ...) is not available urlparse wont work
    if loc.scheme == "":
        url = "http://" + url
        loc = urlparse(url)
    return loc


def _http_connect(loc):
    """Connects to the host and returns an HTTP or HTTPS connections."""
    if loc.scheme == "https":
        ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_SSLv23)
        return http.client.HTTPSConnection(loc.netloc, context=ssl_context)
    return http.client.HTTPConnection(loc.netloc)


def _http_request(loc, get_request=False):
    """Performs a HTTP request and return response in a Result object.

    Does a HEAD HTTP request if get_request is False and GET if True.
    """
    conn = _http_connect(loc)
    method = 'GET' if get_request else 'HEAD'

    conn.request(method, loc.path)
    resp = conn.getresponse()

    result = Result(loc.geturl())
    result.status = resp.status
    result.desc = resp.reason
    result.fill_headers(resp.getheaders())

    # status code is not 204 (no content) and not a redirect
    if get_request and resp.status not in (204, 301, 302, 303, 307, 308):
        result.content = resp.read().decode('utf-8')

    conn.close()
    return result


def http_response(url, parse=False):
    """Returns the HTTP response code.

    If the response code is a temporary or permanent redirect then it
    follows to the redirect URL and returns its response code.

    If parse is False(default) just the URL's header will be requested. If
    it's True then the content will be downloaded for parsing the sitemap
    data.

    Returns a tuple containing HTTP response code and description.
    """
    loc = parse_url(url)
    result = Result(url=url)

    try:
        start = timeit.default_timer()
        get_request = parse and url.endswith('.xml')
        result = _http_request(loc, get_request=get_request)
        result.latency = '{:2.3}'.format(timeit.default_timer() - start)

        # if response code is a HTTP redirect then follow it recursively
        if result.status in (301, 302, 303, 307, 308):
            # if URL in Location is a relative URL, ie starts with a /, then
            # reconstruct the new URL using the current one's scheme and host
            new_url = result.headers.get('Location')
            if new_url.startswith('/'):
                new_url = '{}://{}{}'.format(loc.scheme, loc.netloc, new_url)
            result.redirect = http_response(new_url, parse=parse)

        if result.content:
            sitemap = urls_from_xml(result.content)
            result.sitemap_urls = []
            for s_url in sitemap:
                # some sites include the sitemap's url in the sitemap
                if s_url == result.url:
                    continue
                result.sitemap_urls.append(http_response(s_url, parse=parse))

    except socket.gaierror:
        result.desc = 'Could not resolve'
    return result
