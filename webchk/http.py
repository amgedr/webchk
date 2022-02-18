import http.client
from urllib.parse import urlparse
import socket
import ssl
import sys
import timeit

from . import __version__
from webchk.utils import urls_from_xml


class HTTPRequests:
    def __init__(self, urls, output_file=sys.stdout, list_only=False,
                 parse_xml=False, timeout=3, show_headers=False,
                 headers=None, get_request=False, auth=None,
                 user_agent=None) -> None:
        self.urls = urls
        self.output_file = output_file
        self.list_only = list_only
        self.parse_xml = parse_xml
        self.timeout = timeout
        self.get_request = get_request
        self.show_headers = show_headers

        self.headers = headers if headers is not None else {}
        if not user_agent:
            user_agent = f'webchk v{__version__}'
        self.headers['User-Agent'] = user_agent
        if auth:
            self.headers['Authorization'] = auth


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
        return '{} ... {} {} ({})'.format(
            self.url, self.status, self.desc, self.latency
        )

    def fill_headers(self, headers):
        """Takes a list of tuples and converts it a dictionary."""
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


def _http_connect(loc, timeout):
    """Connects to the host and returns an HTTP or HTTPS connections."""
    if loc.scheme == "https":
        ssl_context = ssl.SSLContext()
        return http.client.HTTPSConnection(
            loc.netloc, context=ssl_context, timeout=timeout)
    return http.client.HTTPConnection(loc.netloc, timeout=timeout)


def _http_request(loc, req: HTTPRequests):
    """Performs a HTTP request and return response in a Result object."""
    conn = None
    try:
        conn = _http_connect(loc, req.timeout)
        method = 'GET' if req.get_request or req.parse_xml else 'HEAD'

        conn.request(method, loc.path, headers=req.headers)
        resp = conn.getresponse()

        result = Result(loc.geturl())
        result.status = resp.status
        result.desc = resp.reason
        result.fill_headers(resp.getheaders())

        # status code is not 204 (no content) and not a redirect
        is_not_redirect = resp.status not in (204, 301, 302, 303, 307, 308)
        if (req.get_request or req.parse_xml) and is_not_redirect:
            result.content = resp.read()

    except TimeoutError:
        raise
    finally:
        if conn:
            conn.close()
    return result


def http_response(url, requests: HTTPRequests):
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

        result = _http_request(loc, requests)
        result.latency = '{:2.3}'.format(timeit.default_timer() - start)

        if 400 <= result.status < 500:
            return result

        # if response code is a HTTP redirect then follow it recursively
        if result.status in (301, 302, 303, 307, 308):
            # if URL in Location (or location) is a relative URL, ie starts
            # with a /, then reconstruct the new URL using the current one's
            # scheme and host
            if 'Location' in result.headers:
                new_url = result.headers.get('Location')
            elif 'location' in result.headers:
                new_url = result.headers.get('location')

            if not new_url:
                result.desc = 'Redirect location not set'
            elif new_url == result.url:
                result.desc = 'URL redirecting to itself'
            else:
                if new_url.startswith('/'):
                    new_url = '{}://{}{}'.format(
                        loc.scheme, loc.netloc, new_url)
                result.redirect = http_response(new_url, requests)

        if result.content and requests.parse_xml:
            requests.parse_xml = False
            sitemap = urls_from_xml(result.content)
            result.sitemap_urls = []
            for s_url in sitemap:
                # some sites include the sitemap's url in the sitemap
                if s_url == result.url:
                    continue
                result.sitemap_urls.append(http_response(s_url, requests))

    except socket.gaierror:
        result.desc = 'Could not resolve'
    except (TimeoutError, socket.timeout):
        result.desc = 'Operation timed out'
    except http.client.RemoteDisconnected as exc:
        result.desc = str(exc)
    except http.client.InvalidURL:
        result.desc = 'Invalid URL'
    except (ConnectionRefusedError, ConnectionResetError) as exc:
        result.desc = exc.strerror
    except ssl.SSLCertVerificationError as exc:
        result.desc = exc.verify_message
    except ssl.SSLError:
        result.desc = 'SSL is misconfigured'
    return result
