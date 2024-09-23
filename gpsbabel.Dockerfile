FROM ubuntu:latest

RUN apt-get update && apt-get install -y gpsbabel && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["gpsbabel"]
