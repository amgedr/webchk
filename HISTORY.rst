=======
History
=======

1.2.1 (2022-02-23)
------------------
* Limit number of redirections


1.2.0 (2022-02-19)
------------------

* Default HTTP method is now HEAD
* Added --get to switch to HTTP GET
* Added --agent to set the User-Agent
* Added --auth for adding Authorization header
* Prevent timeouts less than 1
* Display results immediately instead of at the end


1.1.0 (2022-02-05)
------------------

* Handle connection related errors
* Improve reporting of HTTP redirects
* Added --timeout or -t to modify respose deadline


1.0.4 (2020-08-29)
------------------

* Fix crash when an URL check times out
* Fix --output command-line option


1.0.3 (2020-07-10)
------------------

* Modify the Python versions tox tests
* Fix failing unit tests


1.0.2 (2020-05-08)
------------------

* Add Python versions 3.7 and 3.8 to the list of tested versions


1.0.1 (2020-05-08)
------------------

* Fixed: Parsing sitemaps enters an endless loop
* Fixed: Parsing a URL that does not exists exits with an unhandled exception


1.0.0 (2018-12-06)
------------------

* Linked to http://codehill.com/projects/webchk/ instead of readthedocs.io


0.3.0 (2018-03-24)
------------------

* Run each check in its own thread


0.2.1 (2017-12-19)
------------------

* Fixed: Status code description not being displayed
* Improved PyPI and GitHub README


0.2.0 (2017-12-14)
------------------

* Code refactoring
* Created setup.py

