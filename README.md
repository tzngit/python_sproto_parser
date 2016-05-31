# python_sproto_parser
a sproto parser wrriten in python

a parser for [sproto](https://github.com/cloudwu/sproto), but don't support encode/decode, just a parser which parsing .sproto text
into python dict.dump already added. :blush:

Examples:

run ```python test.py your_sproto_file.sproto``` to see parse result.

dump to binary file usage:
```
usage: sprotodump.py [-h] [-d SRC_DIR] [-f SRC_FILE] [-o OUTFILE] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -d SRC_DIR, --directory SRC_DIR
                        sproto source files
  -f SRC_FILE, --file SRC_FILE
                        sproto single file
  -o OUTFILE, --out OUTFILE
                        specific dump binary file
  -v, --verbose         show more info
```
