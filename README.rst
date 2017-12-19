======
webchk
======


.. image:: https://img.shields.io/pypi/v/webchk.svg
        :target: https://pypi.python.org/pypi/webchk

.. image:: https://img.shields.io/travis/amgedr/webchk.svg
        :target: https://travis-ci.org/amgedr/webchk

.. image:: https://readthedocs.org/projects/webchk/badge/?version=latest
        :target: https://webchk.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/amgedr/webchk/shield.svg
     :target: https://pyup.io/repos/github/amgedr/webchk/
     :alt: Updates

.. image:: https://readthedocs.org/projects/webchk/badge/?version=latest
     :target: http://webchk.readthedocs.io/en/latest/?badge=latest
     :alt: Documentation Status

webchk is a command-line tool for checking the HTTP status codes and response
header of URLs. It accepts one or more URLs as arguments as well as a sitemap
URL to download, extract the URLs in it and check their statuses. It's also
open source with a MIT license.


Installation
------------
webchk is available on PyPI and can be installed using pip with the following
command::

    $ pip install webchk


Usage
-----
::

 webchk [-h] [-i INPUT] [-o OUTPUT] [-p] [-a] [-l] [-s] [-f] [-v]
              [urls [urls ...]]

 positional arguments:
   urls

 optional arguments:
   -h, --help                   show this help message and exit
   -i INPUT, --input INPUT      Read input from a file
   -o OUTPUT, --output OUTPUT   Save output to a file
   -p, --parse                  Follow links listed in .xml URLs
   -l, --list                   Print URLs without checking them
   -v, --version                Print the version number


Examples
~~~~~~~~
Check a list of URLs from a file (one URL per line)::

    $ webchk -i urls.txt

Check the status of a sitemap file and all the URLs listed in it::

    $ webchk -p http://example.com/sitemap.xml

List the URLs in a file without checking their HTTP status::

    $ webchk -li urls.txt

Check the URLs in a file and .xml files in it::

    $ webchk -pi urls.txt

List the URLs in a file and .xml files in it::

    $ webchk -pli urls.txt

List the URLs in a sitemap without checking their status::

    $ webchk -lp http://example.com/sitemap.xml

