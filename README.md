# TCX to KML
This CLI tool uses [tcxreader](https://github.com/alenrajsp/tcxreader) and the ElementTree XML API to read TCX files and output KML files


## Installation
You can install `tcxreader` through pip
~~~pip install tcxreader
~~~




## Flags
~~~
tcx_to_kml.py [-h] [--o O] [--r | --s] [--path | --points] file_path

options:
  -h, --help  show this help message and exit
  --o O       file output location, defaults to 'output'
  --r         prints activity info, doesn't read/write track data
  --s         silent mode; no activity related data will print
  --path      only writes path KML
  --points    only writes points KML
~~~
