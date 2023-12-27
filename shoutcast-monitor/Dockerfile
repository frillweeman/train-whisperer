FROM python:3.8-slim-buster

WORKDIR /app
RUN mkdir /app/recordings
COPY . /app

# Install ffmpeg as dependency of pydub
RUN apt-get update && \
    apt-get install -y ffmpeg

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "async_server.py"]
