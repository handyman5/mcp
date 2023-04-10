#!/usr/bin/env python

import queue
import sys
import tempfile
import time
import urllib.parse

import pyttsx3
import requests
import sounddevice as sd
import soundfile as sf

from faster_whisper import WhisperModel
from sseclient import SSEClient


def speak(message):
    # from https://pyttsx3.readthedocs.io/en/latest/engine.html#examples
    if not message:
        return
    engine = pyttsx3.init()
    engine.startLoop(False)
    print(f"Speaking: '{message}'")
    engine.say(message)
    while True:
        engine.iterate()
        time.sleep(0.1)
        if not engine.isBusy():
            break
    engine.endLoop()


def record():
    # from https://python-sounddevice.readthedocs.io/en/0.4.6/usage.html#recording
    q = queue.Queue()

    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())


    output = tempfile.NamedTemporaryFile(suffix=".wav")
    try:
        device_info = sd.query_devices(None, "input")
        blocksize = 18000
        channels = 2
        samplerate = int(device_info["default_samplerate"])

        speak(f"Recording; press control C to stop...")

        # Make sure the file is opened before recording anything:
        with sf.SoundFile(
            output, mode="x", samplerate=samplerate, channels=channels
        ) as file:
            with sd.InputStream(
                samplerate=samplerate,
                blocksize=blocksize,
                channels=channels,
                callback=callback,
            ):
                while True:
                    file.write(q.get())
    except KeyboardInterrupt:
        speak("Finished recording")
        return output


def transcribe(audio_file_object):
    # from https://github.com/guillaumekln/faster-whisper
    speak("Recognizing voice input...")

    model_size = "large-v2"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(audio_file_object.name, beam_size=5)

    return "".join(x.text for x in segments)


def get_conversation():
    results = requests.get("http://localhost:8008/api/chat/")
    try:
        conversation = results.json()[0]["id"]
    except Exception:
        results2 = requests.post(
            "http://localhost:8008/api/chat/?temp=0.1&top_k=50&max_length=256&top_p=0.95&ctx_length=512&repeat_last_n=64&model=7B&n_threads=4&repeat_penalty=1.3&init_prompt=Below+is+an+instruction+that+describes+a+task.+Write+a+response+that+appropriately+completes+the+request.+The+response+must+be+accurate%2C+concise+and+evidence-based+whenever+possible.+A+complete+answer+is+always+ended+by+%5Bend+of+text%5D."
        )
        conversation = results2.json()

    return conversation


def ask(question):
    # from https://pyttsx3.readthedocs.io/en/latest/engine.html#examples
    speak(f"You asked me: {question}")
    speak("Thinking...")

    conversation = get_conversation()

    messages = SSEClient(
        f"http://localhost:8008/api/chat/{conversation}/question?prompt={urllib.parse.quote_plus(question)}"
    )

    response = ""
    # words = []
    for msg in messages:
        print(f"Received message: '{msg.data}'")
        if msg.event == "ping":
            print("Ping, skipping...")
            continue
        if msg.event == "close":
            #speak("".join(words))
            print()
            print("Message is done!")
            speak(response)
            print(f"Response was: {response}")
            sys.exit()
        if not msg.data:
            print("Empty response, skipping...")
            continue
        response += msg.data
        # words.append(msg.data)
        # if " " in "".join(words):
        #     split_words = "".join(words).split(" ")
        #     sentence = " ".join(split_words[0:-1])
        #     words = [split_words[-1]]
        #     speak(sentence.strip())


if __name__ == "__main__":
    result = record()
    question = transcribe(result)
    ask(question)
