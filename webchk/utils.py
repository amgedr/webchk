import argparse
from xml.etree import ElementTree

from . import __cmd_description__


def get_parser():
    """Command-line argument help"""
    parser = argparse.ArgumentParser(
        prog='webchk',
        description=__cmd_description__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument('urls', nargs='*')
    parser.add_argument('-i', '--input', help='Read input from a file')
    parser.add_argument('-o', '--output', help='Save output to a file')
    parser.add_argument(
        '-p', '--parse',
        help='Follow links listed in .xml URLs',
        action='store_true'
    )
    parser.add_argument(
        '-a', '--all',
        help='Display the complete response HTTP header',
        action='store_true'
    )
    parser.add_argument(
        '--get',
        help='Perform HTTP GET request instead of HEAD',
        action='store_true',
    )
    parser.add_argument(
        '--agent',
        help='Set a custom user-agent',
        type=str,
        default='',
    )
    parser.add_argument(
        '-l', '--list',
        help='Print URLs without checking them',
        action='store_true'
    )
    parser.add_argument(
        '-t', '--timeout',
        help='Response deadline in seconds (default is 3)',
        type=int,
        default=3,
    )
    parser.add_argument(
        '-s', '--summary',
        help='Print a summary only',
        action='store_true'
    )
    parser.add_argument(
        '-f', '--format',
        help='Format the URLs heirarchically',
        action='store_true'
    )
    parser.add_argument(
        '-v', '--version',
        help='Print the version number',
        action='store_true'
    )
    return parser


def read_input_file(infile):
    """Return the contents of the file in a list.

    The only filtering done is the removal of empty lines.
    """
    with open(infile) as inf:
        lines = [line.strip() for line in inf if line.strip()]
    return lines


def urls_from_xml(data):
    """Returns a list of URLs extracted from the XML string passed."""
    rootxml = ElementTree.fromstring(data)
    urls = []
    for i in rootxml:
        for j in i:
            if j.tag.endswith("loc"):
                urls.append(j.text.strip())
    return urls


def format_headers(headers: dict) -> str:
    if not isinstance(headers, dict):
        raise ValueError

    indent = ' '
    formatted = []
    for key, val in headers.items():
        formatted.append('{}{}: {}'.format(indent, key, val))
    return '\n'.join(formatted)
