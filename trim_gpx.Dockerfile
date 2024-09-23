FROM python:3.9-slim
RUN pip install gpxpy
ADD trim_gpx.py /usr/local/bin/trim_gpx.py
RUN chmod +x /usr/local/bin/trim_gpx.py
ENTRYPOINT ["python", "/usr/local/bin/trim_gpx.py"]
