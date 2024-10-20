# trim_gpx.py

import argparse
import gpxpy
import math
import re

def parse_coordinate(coord_str):
    # Remove any whitespace
    coord_str = coord_str.strip()

    # Check for suffix N/S/E/W
    if coord_str[-1].upper() in ('N', 'S', 'E', 'W'):
        suffix = coord_str[-1].upper()
        number = coord_str[:-1]
        value = float(number)
        if suffix == 'N':
            if value < 0:
                value = -value  # North latitude should be positive
        elif suffix == 'S':
            if value > 0:
                value = -value  # South latitude should be negative
        elif suffix == 'E':
            if value < 0:
                value = -value  # East longitude should be positive
        elif suffix == 'W':
            if value > 0:
                value = -value  # West longitude should be negative
    else:
        value = float(coord_str)

    return value

def parse_radius(radius_str):
    # Remove any whitespace
    radius_str = radius_str.strip()

    # Extract number and unit
    match = re.match(r'^([0-9.]+)\s*(mi|km)?$', radius_str, re.IGNORECASE)
    if not match:
        raise ValueError(f"Invalid radius format: {radius_str}")

    number = float(match.group(1))
    unit = match.group(2).lower() if match.group(2) else 'mi'  # default to miles

    if unit == 'mi':
        radius_miles = number
    elif unit == 'km':
        radius_miles = number * 0.621371  # convert km to miles
    else:
        raise ValueError(f"Unknown unit: {unit}")

    return radius_miles

def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    R = 3958.8  # Radius of the Earth in miles
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2.0)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2.0)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def trim_gpx(input_file, output_file, trim_start_points, trim_end_points, exclude_locations=None):
    with open(input_file, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            # Trim start and end points
            points = segment.points[trim_start_points:len(segment.points)-trim_end_points]
            # Remove points within exclude locations
            if exclude_locations:
                new_points = []
                for point in points:
                    exclude = False
                    for loc in exclude_locations:
                        distance = haversine_distance(point.latitude, point.longitude, loc['lat'], loc['lon'])
                        if distance <= loc['radius_miles']:
                            exclude = True
                            break
                    if not exclude:
                        new_points.append(point)
                segment.points = new_points
            else:
                segment.points = points

    with open(output_file, 'w') as f:
        f.write(gpx.to_xml())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trim GPX file points.")
    parser.add_argument("--input", required=True, help="Input GPX file path.")
    parser.add_argument("--output", required=True, help="Output GPX file path.")
    parser.add_argument("--trim-start-points", type=int, required=True, help="Number of points to trim from the start.")
    parser.add_argument("--trim-end-points", type=int, required=True, help="Number of points to trim from the end.")
    parser.add_argument("--exclude-location", action='append', help="Exclude location specified as 'lat,lon,radius', e.g., '47.6061N,-122.3328W,0.025mi'. Units for radius can be 'mi' or 'km'.")

    args = parser.parse_args()

    exclude_locations = []
    if args.exclude_location:
        for loc_str in args.exclude_location:
            # loc_str is expected to be 'lat,lon,radius'
            try:
                lat_str, lon_str, radius_str = loc_str.split(',')
            except ValueError:
                raise ValueError(f"Invalid exclude-location format: {loc_str}. Expected format 'lat,lon,radius'.")
            lat = parse_coordinate(lat_str)
            lon = parse_coordinate(lon_str)
            radius_miles = parse_radius(radius_str)
            exclude_locations.append({'lat': lat, 'lon': lon, 'radius_miles': radius_miles})

    trim_gpx(args.input, args.output, args.trim_start_points, args.trim_end_points, exclude_locations)
