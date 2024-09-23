#!/bin/bash

ride=$1
ride_trimmed=${ride}.trim.gpx
trim_start=$2
trim_end=$3
animation=${ride_trimmed}.mp4

docker run --rm -v $(pwd)/data:/data trim-gpx \
  --input /data/${ride} \
  --output /data/${ride_trimmed} \
  --trim-start-points ${trim_start} \
  --trim-end-points ${trim_end}

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
  --zoom 12 \
  --background-map-visibility 0.95 \
  --tms-url-template "https://{switch:a,b,c}.tile.openstreetmap.org/{zoom}/{x}/{y}.png"

echo "wrote ${PWD}/data/${animation}"
