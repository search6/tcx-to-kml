# TCX to KML
CLI tool that uses [tcxreader](https://github.com/alenrajsp/tcxreader) and the ElementTree XML API to read TCX files and convert them to KML files

## Dependency
`tcxreader` is needed and can be installed through pip.
~~~
pip install tcxreader
~~~

## Usage
~~~
usage: tcx_to_kml.py [-h] [-o O] [-v] [--path | --points] [--no_write] file_path

Convert TCX to KML using Trackpoint data

positional arguments:
  file_path   .tcx file to convert to .kml

flags:
  -h, --help  show this help message and exit
  -o O        file output location, defaults to 'output' folder
  -v          verbose; activity related data will print
  --path      only writes path KML
  --points    only writes points KML
  --no_write  does not write any KML files
~~~

## Example
Using an example from the examples folder:
~~~
py .\tcx_to_kml.py examples\running_activity.tcx -v
~~~
~~~
Activity Type: Running

Start Date & Time: 2014-12-26 10:55:09 UTC
Total Distance: 14332.28 meters (8.91 miles)
Time Elasped: 0 hours 54 minutes 30 seconds

Calories: 1182
Heart Rate Info:
    Average: 176.66 BPM
    Minimum: 113 BPM
    Maximum: 181 BPM

Points KML outputted at '~\output\running_activity_points.kml'
Path KML outputted at '~\output\running_activity_path.kml'
~~~


`tcx_to_kml.py` reads the activity information in the file, and creates two files: `file_name_points.kml` & `file_name_path.kml`.
General activity information can be printed with the `-v` flag.

`running_activity_path.kml` is shown below.
~~~kml
<?xml version='1.0' encoding='UTF-8'?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
	<Document>
		<name>running_activity_1</name>
		<Style id="lineStyle">
			<LineStyle>
				<width>2</width>
			</LineStyle>
		</Style>
		<Placemark>
			<styleUrl>#lineStyle</styleUrl>
			<LookAt>
				<latitude>46.116950707510114</latitude>
				<longitude>14.672594759613276</longitude>
				<heading>0</heading>
				<tilt>0</tilt>
				<range>1500</range>
				<altitudeMode>clampToGround</altitudeMode>
			</LookAt>
			<LineString>
        			<coordinates>...</coordinates>
			</LineString>
		</Placemark>
	</Document>
</kml>
~~~
