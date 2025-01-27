import os
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from tcxreader.tcxreader import TCXReader, TCXTrackPoint, TCXExercise

# points = [(lat, long, title), (tuple2), ...]
def write_point_kml(output_name: str, points: list[TCXTrackPoint], output_path: str | Path) -> None:
    """Writes a point KML file using TCXTrackPoint data from tcxreader"""

    root = ET.Element("kml", {"xmlns": "http://www.opengis.net/kml/2.2", "xmlns:gx": "http://www.google.com/kml/ext/2.2", "xmlns:kml": "http://www.opengis.net/kml/2.2", "xmlns:atom": "http://www.w3.org/2005/Atom"})

    # Document
    document = ET.SubElement(root,"Document")
    ET.SubElement(document, "name").text = output_name # Document name

    # Style
    style = ET.SubElement(document, "Style", {"id": "data+icon"})

    # BallonStyle
    balloon_style = ET.SubElement(style, "BalloonStyle")
    ET.SubElement(balloon_style, "text")

    # IconStyle
    icon_style = ET.SubElement(style, "IconStyle")
     # Resizes the icon
    ET.SubElement(icon_style, "scale").text = "0.25"
     # Direction of the icon (North, East, South, West) in degrees (0, 360)
    ET.SubElement(icon_style, "heading").text = "0"

    # Icon; defines a image; must have a href element
    icon = ET.SubElement(icon_style, "Icon")
    ET.SubElement(icon, "href").text = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUAQMAAAC3R49OAAAABlBMVEUAAAD///+l2Z/dAAAAEklEQVQImWNgAIL6/w+ogoEAAKI4Kp2NVIeDAAAAAElFTkSuQmCC"

    # hotSpot; Offsets the position the icon
    ET.SubElement(icon_style, "hotSpot", {"x": "0.5", "y":"0.5", "xunits":"fraction", "yunits":"fraction"})

    # Writes all points
    for point in points:

        placemark = ET.SubElement(document, "Placemark")
         # styleUrl; Applies changes defined in the Style element
        ET.SubElement(placemark, "styleUrl").text = "#data+icon"
         # Title for each point
        ET.SubElement(placemark, "name").text = str(point.distance)

        # LookAt
        look_at = ET.SubElement(placemark, "LookAt")
        ET.SubElement(look_at, "latitude").text = str(points[0].latitude)
        ET.SubElement(look_at, "longitude").text = str(points[0].longitude)
        ET.SubElement(look_at, "heading").text = "0"
        ET.SubElement(look_at, "tilt").text = "0"
        ET.SubElement(look_at, "range").text = "1500"
        ET.SubElement(look_at, "altitudeMode").text = "clampToGround"

        # Point
        point_element = ET.SubElement(placemark, "Point")

        # why does KML make longitude first??
        # confusing for no reason whatsoever
        # https://developers.google.com/kml/documentation/kmlreference#linestring
        ET.SubElement(point_element, "coordinates").text = f"{point.longitude},{point.latitude},0 "


    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)

    # Write KML to file
    with open(output_path, 'wb') as file:
        tree.write(file, "UTF-8", True)
        print(f"Points KML outputted at '{output_path}'")


def write_path_kml(output_name: str, points: list[TCXTrackPoint], output_path: str | Path) -> None:
    """Writes path KML file using TCXTrackPoint data from tcxreader"""

    root = ET.Element("kml", {"xmlns": "http://www.opengis.net/kml/2.2", "xmlns:gx": "http://www.google.com/kml/ext/2.2", "xmlns:kml": "http://www.opengis.net/kml/2.2", "xmlns:atom": "http://www.w3.org/2005/Atom"})

    # Document
    document = ET.SubElement(root,"Document")
     # Document name
    ET.SubElement(document, "name").text = output_name

    # Style
    style = ET.SubElement(document, "Style", {"id": "lineStyle"})

    # LineStyle
    line_style = ET.SubElement(style, "LineStyle")
     # line width
    ET.SubElement(line_style, "width").text = "2"

    # Placemark
    placemark = ET.SubElement(document, "Placemark")
     # styleUrl; Applies changes defined in Style element
    ET.SubElement(placemark, "styleUrl").text = "#lineStyle"

    # LookAt
    look_at = ET.SubElement(placemark, "LookAt")
    ET.SubElement(look_at, "latitude").text = str(points[0].latitude)
    ET.SubElement(look_at, "longitude").text = str(points[0].longitude)
    ET.SubElement(look_at, "heading").text = "0"
    ET.SubElement(look_at, "tilt").text = "0"
    ET.SubElement(look_at, "range").text = "2000"
    ET.SubElement(look_at, "altitudeMode").text = "clampToGround"

    # Line String
    line_string = ET.SubElement(placemark, "LineString")
    coordinates = ET.SubElement(line_string, "coordinates")

    coords = []
    for point in points:
        # Write longitude, latitude, altitude to the <coordinates> tag
        coords.append(f"{point.longitude},{point.latitude},0 ")
    coordinates.text = "".join(coords)


    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)

    with open(output_path, 'wb') as file:
        tree.write(file, "UTF-8", True)
        print(f"Path KML outputted at '{output_path}'")


def read_tcx_file(file_path: Path, *, print_activity_info=False) -> list[TCXTrackPoint]:
    """Reads a .tcx file & returns trackpoints. Can also print light activity data."""

    tcx_reader = TCXReader()
    data: TCXExercise = tcx_reader.read(str(file_path))

    if print_activity_info:
        elasped_time = data.duration
        m, s = divmod(elasped_time, 60)
        h, m = divmod(m, 60)

        distance_miles = float(data.distance)/1609
        print(f"Activity Type: {data.activity_type}", end="\n\n")
        print(f"Start Date & Time: {data.end_time} UTC")
        print(f"Total Distance: {data.distance:.02f} meters ({distance_miles:.02f} miles)")
        print(f"Time Elasped: {h:.0f} hours {m:.0f} minutes {s:.0f} seconds", end="\n\n")
        print(f"Calories: {'No Calorie Data' if data.calories == 0 else data.calories}")

        if data.hr_avg is not None:
            print(f"""Heart Rate Info:
    Average: {round(data.hr_avg, 2)} BPM
    Minimum: {data.hr_min} BPM
    Maximum: {data.hr_max} BPM""", end="\n\n")

    return data.trackpoints


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert TCX to KML using Trackpoint data")
    parser.add_argument("file_path", help=".tcx file to convert to .kml")
    parser.add_argument('-o', help="file output location, defaults to 'output' folder", default="output")
    parser.add_argument("-v", help="verbose; activity related data will print", action="store_true")

    pg = parser.add_mutually_exclusive_group()
    pg.add_argument("--path", help="only writes path KML", action="store_false")
    pg.add_argument("--points", help="only writes points KML", action="store_false")

    parser.add_argument("--no_write", help="does not write any KML files", action="store_true")

    args = parser.parse_args()

    # File path handling
    input_file_path = Path.cwd().joinpath(args.file_path)
    output_directory = Path.cwd().joinpath(args.o)
    file_name = input_file_path.stem

    # File checks
    if not input_file_path.exists():
        raise FileNotFoundError("File does not exist")

    if not input_file_path.is_file() or input_file_path.suffix != ".tcx":
        raise TypeError("Invalid path or file extension")

    if not output_directory.exists():
        os.mkdir(output_directory)

    # Read trackpoints
    trackpoints: list[TCXTrackPoint] = read_tcx_file(input_file_path, print_activity_info=args.v)

    # Write KML file
    output_path_points = Path.joinpath(output_directory,f"{file_name}_points.kml")
    output_path_path = Path.joinpath(output_directory,f"{file_name}_path.kml")

    if not args.no_write:
        if args.path:
            write_point_kml(file_name, trackpoints, output_path_points)
        if args.points:
            write_path_kml(file_name, trackpoints, output_path_path)
