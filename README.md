# webchk
webchk is an open source Python 3 command-line tool for getting the HTTP response codes and headers of URLs.

### Usage
```
webchk [-alpsf] URL... [-o <file>]
webchk [-alpsf] -i <file> [-o <file>]
webchk -h, --help
webchk -v, --version
```

### Command-line Options
```
-i <file>, --input <file>     Read input from a file
-o <file>, --output <file>    Save output to a file
-p, --parse                   Parse contents of URLs with .xml extention
-a, --all                     Display the complete HTTP header
-l, --list                    Print URLs without checking them
-s, --summary                 Print a summary only
-f, --format                  Format the URLs heirarchically
-h, --help                    Show this
-v, --version                 Print the version number
```

#### Download From GitHub
webchk is in a single file. It can be downloaded and run in any computer that has Python 3 installed.

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
