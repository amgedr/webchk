import sys
import threading
from .utils import get_parser, read_input_file
from .http import http_response
from . import __version__


def _process_url(url, output_file, parse_xml):
    resp = http_response(url, parse=parse_xml)
    print(resp, file=output_file)

    follow = resp.redirect
    while follow:
        print('   {}'.format(follow), file=output_file)
        follow = follow.redirect

    if resp.sitemap_urls:
        for sitemap_url in resp.sitemap_urls:
            print('   {}'.format(sitemap_url), file=output_file)


def process_urls(urls, output_file, list_only=False, parse_xml=False):
    """Loops through the list of URLs and performs the checks.

    output_file is the path to the file that will be written to.

    If list_only is True URLs will just be printed out without checking.

    If parse_xml is True URLs ending with .xml will be treated as sitemap
    files and will be downloaded to search its contents for more URLs to
    check.
    """
    threads = []

    for url in urls:
        if list_only:
            print(url)
            continue

        thread = threading.Thread(
            target=_process_url, args=(url, output_file, parse_xml))
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
        urls = []
        if args.urls:
            urls.extend(args.urls)

        if args.input:
            urls.extend(read_input_file(args.input))

        if args.output:
            output_file = open(args.output, 'w')
        else:
            output_file = sys.stdout

        process_urls(
            urls, output_file, list_only=args.list, parse_xml=args.parse)

        if args.output:
            output_file.close()

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
