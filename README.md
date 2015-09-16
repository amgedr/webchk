# webchk
Get the HTTP response codes and headers of URLs.

### Examples
Check a list of URLs from a file (one URL per line):
```
$ webchk -i urls.txt
```
List the URLs in a file without checking their HTTP status:
```
$ webchk -li urls.txt
```
Check the URLs in a file and .xml files in it:
```
$ webchk -pi urls.txt
```
List the URLs in a file and .xml files in it:
```
$ webchk -pli urls.txt
```
Check the status of a sitemap file and all the URLs listed in it:
```
$ webchk -p http://example.com/sitemap.xml
```
List the URLs in a sitemap without checking their status:
```
$ webchk -lp http://example.com/sitemap.xml   
```
