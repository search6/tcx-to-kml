import sys
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET
from tcxreader.tcxreader import TCXReader

# points = [(lat, long, title), (tuple2), ...]
def write_point_kml(output_name: str, points: list[tuple], *, print_kml=False, output_path="points.kml") -> None: 
    root = ET.Element("kml", {"xmlns": "http://www.opengis.net/kml/2.2", "xmlns:gx": "http://www.google.com/kml/ext/2.2", "xmlns:kml": "http://www.opengis.net/kml/2.2", "xmlns:atom": "http://www.w3.org/2005/Atom"})
    
    # Document
    document = ET.SubElement(root,"Document")
    ET.SubElement(document, "name").text = output_name # Document name
    
    # Style
    style = ET.SubElement(document, "Style", {"id": "data+icon"})
    
    #BallonStyle
    balloon_style = ET.SubElement(style, "BalloonStyle")
    balloon_text = ET.SubElement(balloon_style, "text")
   
    # IconStyle
    icon_style = ET.SubElement(style, "IconStyle")
    ET.SubElement(icon_style, "scale").text = "0.25" # Resizes the icon
    ET.SubElement(icon_style, "heading").text = "0" # Direction of the icon (North, East, South, West) in degrees (0, 360)
    
    # Icon; defines a image; must have a href element
    Icon = ET.SubElement(icon_style, "Icon")
    ET.SubElement(Icon, "href").text = "https://upload.wikimedia.org/wikipedia/commons/c/c1/20x20square.png" # Icon link
    
    # hotSpot; Offsets the position the icon
    ET.SubElement(icon_style, "hotSpot", {"x": "0.5", "y":"0.5", "xunits":"fraction", "yunits":"fraction"})
    
    # Writes all points 
    for point in points:        
        #latitude = point[0]
        #longitude = point[1]
        #distance_elasped = point[2]
        
        placemark = ET.SubElement(document, "Placemark")
        ET.SubElement(placemark, "styleUrl").text = "#data+icon" # styleUrl; Applies changes defined in the Style element
        ET.SubElement(placemark, "name").text = point[2] # Title for each point

        # LookAt
        look_at = ET.SubElement(placemark, "LookAt")
        ET.SubElement(look_at, "latitude").text = points[0][0]
        ET.SubElement(look_at, "longitude").text = points[0][1]
        ET.SubElement(look_at, "heading").text = "0"
        ET.SubElement(look_at, "tilt").text = "0"
        ET.SubElement(look_at, "range").text = "1500"
        ET.SubElement(look_at, "altitudeMode").text = "clampToGround"
        
        # Point
        Point = ET.SubElement(placemark, "Point")
        
        # why does kml make longitude first??
        ET.SubElement(Point, "coordinates").text = f"{point[1]},{point[0]},0"
        
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    
    if not print_kml:
        with open(str(output_path), 'wb') as file:
            tree.write(file, "UTF-8", True)
            print(f"Points KML outputted at {str(output_path)}")
    else:
        tree.write(sys.stdout.buffer, "UTF-8", True)



def write_path_kml(output_name: str, points: list[tuple], *, print_kml=False, output_path="path.kml") -> None:
    root = ET.Element("kml", {"xmlns": "http://www.opengis.net/kml/2.2", "xmlns:gx": "http://www.google.com/kml/ext/2.2", "xmlns:kml": "http://www.opengis.net/kml/2.2", "xmlns:atom": "http://www.w3.org/2005/Atom"})
    
    # Document
    document = ET.SubElement(root,"Document")
    ET.SubElement(document, "name").text = output_name # Document name
    
    # Style
    style = ET.SubElement(document, "Style", {"id": "lineStyle"}) 
    
    # LineStyle
    line_style = ET.SubElement(style, "LineStyle")
    ET.SubElement(line_style, "width").text = "2" # Line Width

    # Placemark
    placemark = ET.SubElement(document, "Placemark")
    ET.SubElement(placemark, "styleUrl").text = "#lineStyle" # styleUrl; Applies changes defined in Style element 
    
    # LookAt
    look_at = ET.SubElement(placemark, "LookAt")
    ET.SubElement(look_at, "latitude").text = points[0][0]
    ET.SubElement(look_at, "longitude").text = points[0][1]
    ET.SubElement(look_at, "heading").text = "0"
    ET.SubElement(look_at, "tilt").text = "0"
    ET.SubElement(look_at, "range").text = "1500"
    ET.SubElement(look_at, "altitudeMode").text = "clampToGround"
    
    # Line String
    line_string = ET.SubElement(placemark, "LineString")
    coordinates = ET.SubElement(line_string, "coordinates")
    coordinates.text = ""
    
    # confusing for no reason whatsoever
    # https://developers.google.com/kml/documentation/kmlreference#linestring:~:text=%3Ccoordinates%3E...%3C/coordinates%3E%20%20%20%20%20%20%20%20%20%20%20%20%3C!%2D%2D%20lon%2Clat%5B%2Calt%5D%20%2D%2D%3E
    
    coords = []
    for point in points:
        # latitude = point[0]
        # longitude = point[1]
        # Write longitude, latitude, altitude to the coordinates tag
        coords.append(f"{point[1]},{point[0]},0 ")
    coordinates.text = "".join(coords) 
    
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    
    if not print_kml:
        with open(output_path, 'wb') as file:
            tree.write(file, "UTF-8", True)
            print(f"Path KML outputted at {output_path}")
    else:
        tree.write(sys.stdout.buffer, "UTF-8", True)


def read_tcx_file(file_path: str | Path, *, read_trackpoints=False, silent=False) -> None | list[tuple] :
    file_path = Path(file_path)
    try:
        # Checks if file is a .tcx file
        if file_path.suffix != ".tcx":
            raise Exception("Exception: Invalid file extension")

        tcx_reader = TCXReader()
        data = tcx_reader.read(str(file_path))
        
        a_type = data.activity_type
        a_date = str(data.end_time) + " UTC"
        a_TotalTime = int(data.duration)
        a_m, a_s = divmod(a_TotalTime, 60)
        a_h, a_m = divmod(a_m, 60)
        a_distance = data.distance
        a_distance_miles = float(a_distance)/1609     
        a_calories = data.calories
        a_AvgHeartRate = data.hr_avg
        a_MinHearRate = data.hr_min
        a_MaxHeartRate = data.hr_max
        
        
        if not silent:
            print(f"Activity Type: {a_type}", end="\n\n")
            print(f"Start Date & Time: {a_date}")
            print(f"Total Distance: {round(a_distance, 2)} meters ({round(a_distance_miles, 2)} miles)")
            print(f"Time Elasped: {a_h} hours {a_m} minutes {a_s} seconds", end="\n\n")
            print(f"Calories: {'No Calorie Data' if a_calories == 0 else a_calories}")
            print(f"Heart Rate Info: \n\tAverage: {a_AvgHeartRate} BPM \n\tMinimum: {a_MinHearRate} BPM \n\tMaximum: {a_MaxHeartRate} BPM", end="\n\n")
 
        if read_trackpoints:
            tkpoints = []
            for tkp in data.trackpoints:
                tkpoints.append((str(tkp.latitude), str(tkp.longitude), str(tkp.distance)))
            return tkpoints
            
    except FileNotFoundError as err:
        print(f"No such file or directory: '{err.filename}'")
    except Exception as err:
        print(err)


def write_kml_file(file_name, coordinates: list[tuple], *, output_point_kml=True, output_path_kml=True, output_directory):
    # write_point_kml & write_path_kml have the same args
    # - file name
    # - list of tuples containing latitude, longitude, and title
    # - flag to print kml to console (defaults to False)
    # - output path for file (defaults to "output\file.kml")
    

    if output_point_kml: write_point_kml(file_name, coordinates, output_path=Path.joinpath(output_directory,f"{file_name}_points.kml"))
    if output_path_kml: write_path_kml(file_name, coordinates, output_path=Path.joinpath(output_directory,f"{file_name}_path.kml"))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert to KML using TCX Trackpoint Position data")
    parser.add_argument("file_path", help="file to convert to KML")
    parser.add_argument('-o', help="file output location, defaults to 'output'", default="output")
    
    pg1 = parser.add_mutually_exclusive_group()
    pg1.add_argument("-r", help="prints activity info, doesn't read/write track data", action="store_true")
    pg1.add_argument("-s", help="silent mode; no activity related data will print", action="store_true")
    
    pg2 = parser.add_mutually_exclusive_group()
    pg2.add_argument("-path", help="only writes path KML", action="store_false")
    pg2.add_argument("-points", help="only writes points KML", action="store_false")
    
    args = parser.parse_args()
    
    # File path handling
    input_file_path = Path.cwd().joinpath(args.file_path)
    file_name = input_file_path.stem
    file_extension = input_file_path.suffix
    output_directory = Path.cwd().joinpath(args.o)

    # Check if file exists
    if input_file_path.exists():

        # Read trackpoints; if data isn't read, read_tcx_file doesn't returns None
        trackpoints: list[tuple] | None = read_tcx_file(input_file_path, read_trackpoints=(not args.r), silent=args.s) 
 
        # Check if trackpoints is empty and write KML files
        if not args.r:
            if trackpoints is None:
                print("trackpoints is empty")
            else: write_kml_file(file_name, trackpoints, output_point_kml=args.path, output_path_kml=args.points, output_directory=output_directory)