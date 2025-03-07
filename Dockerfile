FROM python:3.11

RUN apt update && apt install -y ffmpeg

RUN python -m pip install faster-whisper
RUN python -m pip install pydub

WORKDIR /app