# Python Video Transcriber

## Getting Start

### Windows

Before execute, install libraries in local environment by running in Windows PowerShell:

`docker run --rm -w /app -v ${pwd}:/app python:3.11 python -m pip install -r requirements.txt -t . --upgrade`

then run:

`docker run --rm -w /app -v ${pwd}:/app python:3.11 python transcribe.py`
