import argparse
import gpxpy

def trim_gpx(input_file, output_file, trim_start_points, trim_end_points):
    with open(input_file, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            segment.points = segment.points[trim_start_points:len(segment.points)-trim_end_points]

    with open(output_file, 'w') as f:
        f.write(gpx.to_xml())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trim GPX file points.")
    parser.add_argument("--input", required=True, help="Input GPX file path.")
    parser.add_argument("--output", required=True, help="Output GPX file path.")
    parser.add_argument("--trim-start-points", type=int, required=True, help="Number of points to trim from the start.")
    parser.add_argument("--trim-end-points", type=int, required=True, help="Number of points to trim from the end.")
    
    args = parser.parse_args()
    
    trim_gpx(args.input, args.output, args.trim_start_points, args.trim_end_points)
