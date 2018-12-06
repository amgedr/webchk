======
webchk
======


.. image:: https://img.shields.io/pypi/v/webchk.svg
        :target: https://pypi.org/project/webchk/

.. image:: https://img.shields.io/travis/amgedr/webchk.svg
        :target: https://travis-ci.org/amgedr/webchk

.. image:: https://img.shields.io/github/license/amgedr/webchk.svg
        :target: https://github.com/amgedr/webchk/blob/master/LICENSE

webchk is a command-line tool developed in Python 3 for checking the HTTP
status codes and response headers of URLs. It accepts one or more URLs as
arguments. Furthermore, a sitemap URL can be passed using the -p option to
download its content, extract the URLs and check their statuses.


Installation
------------
webchk is available on PyPI and can be installed using pip with the following
command::

    $ pip install webchk

Webchk does not require any 3rd party packages to run. So it can also be
cloned from GitHub and run as a module::

    $ git clone https://github.com/amgedr/webchk.git
    $ cd webchk
    $ python3 -m webchk

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

