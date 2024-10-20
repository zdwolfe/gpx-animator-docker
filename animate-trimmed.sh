#!/bin/bash

ride=$1
ride_trimmed=${ride}.trim.gpx
exclude_location=$2
animation=${ride_trimmed}.mp4

docker run --rm -v $(pwd)/data:/data trim-gpx \
  --input /data/${ride} \
  --output /data/${ride_trimmed} \
  --exclude-location "${exclude_location}" \
  --trim-start-points 0 --trim-end-points 0

docker run --rm -v $(pwd)/data:/data gpx-animator \
  --input /data/${ride_trimmed} \
  --output /data/${animation} \
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
  --zoom 13 \
  --background-map-visibility 0.95 \
  --tms-url-template "https://{switch:a,b,c}.tile.openstreetmap.org/{zoom}/{x}/{y}.png"

echo "wrote ${PWD}/data/${animation}"
