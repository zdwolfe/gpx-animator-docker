# dockerized tools for animating gpx files

One-liner to trim, then animate a gpx file named ``Evening_Ride.gpx`` in the ``./data`` dir:

```bash
./animate-trimmed.sh Evening_Ride.gpx 40.0002N,-100.000W,0.750mi
```

Syntax:
./animate-trimmed.sh <__input_filename__> <__exclude_location_with_radius__>



# tools
## gpx-animator
Gpx file animation. See https://gpx-animator.app/.


Build:

```bash
docker build -f gpx-animator.Dockerfile -t gpx-animator .
```

Run:

```bash
docker run --rm -v $(pwd)/data:/data gpx-animator \
  --input /data/Lake_Washington_Lollipop.gpx \
  --output /data/output.mp4 \
  --fps 60 \
  --width 1920 \
  --height 1080 \
  --total-time 15000 \
  --line-width 3 \
  --marker-size 10 \
  --tail-color '#FF0000' \
  --speedup 2000.0 \
  --information "%SPEED% %LATLON% %DATETIME%" \
  --information-position BOTTOM_RIGHT \
  --viewport-width 800 \
  --viewport-height 600 \
  --viewport-inertia 100 \
  --track-icon-mirror \
  --comment-margin 30 \
  --skip-idle \
  --pre-draw-track \
  --pre-draw-track-color '#808080' \
  --zoom 12 \
  --background-map-visibility 0.95 \
  --tms-url-template "https://{switch:a,b,c}.tile.openstreetmap.org/{zoom}/{x}/{y}.png"
```






## gpsbabel
Gpx file transformation. See https://www.gpsbabel.org/index.html

Build:

```bash
docker build -f gpsbabel.Dockerfile -t gpsbabel .
```

Run:
```bash
docker run --rm -v $(pwd)/data:/data gpsbabel \
  ...
```

## trim points
Trim points from the beginning and end (to hide "home"). See trim_gpx.py. Can trim "points" and "miles" radius around a GPS coordinate.

```bash
docker build -f trim_gpx.Dockerfile -t trim-gpx .
```

```bash
docker run --rm -v $(pwd)/data:/data trim-gpx \
  --input /data/Lake_Washington_Lollipop.gpx \
  --output /data/Lake_Washington_Lollipop.trim.gpx \
  --trim-start-points 0 --trim-end-points 0 \
  --exclude-location 40.0002N,-100.000W,0.750mi
```
