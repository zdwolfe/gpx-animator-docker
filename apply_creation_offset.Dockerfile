FROM python:3.9-slim
ADD apply_creation_offset.py /usr/local/bin/apply_creation_offset.py
RUN chmod +x /usr/local/bin/apply_creation_offset.py
ENTRYPOINT ["python", "/usr/local/bin/apply_creation_offset.py"]
