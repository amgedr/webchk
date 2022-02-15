import sys
import threading

from .utils import get_parser, read_input_file, format_headers
from .http import http_response, HTTPRequests
from . import __version__


def _process_url(url, requests: HTTPRequests):
    resp = http_response(url, requests)
    print(resp, file=requests.output_file)

    if requests.show_headers:
        print('{}\n'.format(format_headers(resp.headers)))

    follow = resp.redirect
    while follow:
        print('   {}'.format(follow), file=requests.output_file)
        follow = follow.redirect

    if resp.sitemap_urls:
        for sitemap_url in resp.sitemap_urls:
            print('   {}'.format(sitemap_url), file=requests.output_file)


def process_urls(requests: HTTPRequests):
    """Loops through the list of URLs and performs the checks.

    requests.output_file is the path to the file that will be written to.

    If requests.list_only is True URLs will be printed out without checking.

    If requests.parse_xml is True URLs ending with .xml will be treated as
    sitemap files and will be downloaded to search its contents for more URLs
    to check.
    """
    threads = []

    for url in requests.urls:
        if requests.list_only:
            print(url)
            continue

        thread = threading.Thread(
            target=_process_url,
            args=(url, requests)
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def main():
    """Main entry to webchk."""
    parser = get_parser()
    args = parser.parse_args()

    if args.version:
        print(__version__)
        return 0

    if not args.urls and not args.input:
        parser.print_usage()
        return 0

    try:
        requests = HTTPRequests(
            urls=[],
            output_file=open(args.output, 'w') if args.output else sys.stdout,
            list_only=args.list,
            parse_xml=args.parse,
            timeout=args.timeout,
            show_headers=args.all,
            get_request=args.get,
            user_agent=args.agent,
        )

        if args.urls:
            requests.urls.extend(args.urls)

        if args.input:
            requests.urls.extend(read_input_file(args.input))

        process_urls(requests)

        if args.output:
            requests.output_file.close()

    except FileExistsError as ex:
        print(ex, file=sys.stderr)
    except FileNotFoundError as ex:
        print('The file {} does not exist'.format(
            ex.filename), file=sys.stderr)
    except KeyboardInterrupt:
        print('\nProcess cancelled', file=sys.stderr)
    else:
        return 0
    return 1


if __name__ == '__main__':
    sys.exit(main())
