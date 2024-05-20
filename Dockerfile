FROM ubuntu:latest
LABEL authors="skate"

ENTRYPOINT ["top", "-b"]