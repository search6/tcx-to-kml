# TCX to KML
This CLI tool uses [tcxreader](https://github.com/alenrajsp/tcxreader) and the ElementTree XML API to read TCX files and output KML files

## Requirement
`tcxreader` is needed and can be installed through pip.
~~~
pip install tcxreader
~~~

## Usage
Using an example from the examples folder:
~~~
py .\tcx_to_kml.py examples\running_activity.tcx
~~~
~~~
Activity Type: Running

Start Date & Time: 2014-12-26 10:55:09 UTC
Total Distance: 14332.28 meters (8.91 miles)
Time Elasped: 0 hours 54 minutes 30 seconds

Calories: 1182
Heart Rate Info:
        Average: 176.6602870813397 BPM
        Minimum: 113 BPM
        Maximum: 181 BPM

Points KML outputted at ~\output\running_activity_points.kml
Path KML outputted at ~\output\running_activity_path.kml
~~~


`tcx_to_kml.py` reads the activity information in the file, and creates two files: `file_name_points.kml` & `file_name_path.kml`.
General activity information can be ommitted with the `-s` flag.

`running_activity_path.kml` is shown below. Coordinates are ommited for the sake of readability.
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
