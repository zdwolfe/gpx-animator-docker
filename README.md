# docker container for gpx-animator


Build:

```bash
docker build -t gpx-animator .
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


See https://gpx-animator.app/ for all gpx-animator options.
