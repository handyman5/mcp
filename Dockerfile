FROM python:3.11-slim-bullseye

RUN mkdir /app
WORKDIR /app

RUN apt-get update
RUN apt install -y gcc alsa-utils libespeak-ng-libespeak1 portaudio19-dev

RUN pip install faster-whisper
RUN python -c 'from faster_whisper import WhisperModel; model = WhisperModel("large-v2", device="cpu", compute_type="int8")'

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY talker.py /app/talker.py

CMD ["python", "-u", "/app/talker.py"]
