# MCP

## Description

MCP provides a self-hosted, completely offline, voice-only intelligent agent. You can talk to it in conversational language, and it generates an appropriate response and speaks it aloud.

MCP accomplishes this by chaining together:

* [OpenAI's Whisper](https://github.com/openai/whisper) for the voice recognition
* Alpaca LLM by way of [serge](https://github.com/nsarrazin/serge)
* [pyttsx3](https://github.com/nateshmbhat/pyttsx3), an offline text-to-speech converter library

## Current Functionality

MCP can currently do the following:

* When launched, listen to microphone audio until an interrupt signal is received
* Parse that audio and extract the statement or question asked
* Hand that statement or question off to serge to generate an AI response as part of a conversation
* Speak the received response aloud

MCP _cannot_ do any of the following yet (but someday!):

* Listen indefinitely and honor a "Hey, Google"-style wake word
* Listen and speak at the same time
* Run anywhere but Linux (and even that, I've only tested Ubuntu 22.04)

## Prerequisites

Launch [serge](https://github.com/nsarrazin/serge) with:

```
docker run -d -v weights:/usr/src/app/weights -v datadb:/data/db/ -p 8008:8008 ghcr.io/nsarrazin/serge:latest
```

## Usage

```
docker build -t mcp .
docker run --net host --device /dev/snd mcp
```

## Example run

This is an example of the program output for a typical run. Note that anything annotated with `Speaking:` is also spoken aloud by the program.

```
$ docker run --net host --device /dev/snd mcp
Speaking: 'Recording; press control C to stop...'
^CSpeaking: 'Finished recording'
Speaking: 'Recognizing voice input...'
Speaking: 'You asked me:  How much wood could a woodchuck chuck if a woodchuck could chuck wood?'
Speaking: 'Thinking...'
Received message: '2023-04-11 06:35:17.659332'
Ping, skipping...
Received message: '2023-04-11 06:35:32.659348'
Ping, skipping...
Received message: '2023-04-11 06:35:47.659478'
Ping, skipping...
Received message: '2023-04-11 06:36:02.659768'
Ping, skipping...
Received message: '2023-04-11 06:36:17.659668'
Ping, skipping...
Received message: ''
Empty response, skipping...
Received message: 'A'
Received message: ' wood'
Received message: 'ch'
Received message: 'uck'
Received message: ' can'
Received message: ' only'
Received message: ' carry'
Received message: ' around'
Received message: ' one'
Received message: ' p'
Received message: 'ound'
Received message: ' of'
Received message: ' food'
Received message: ' at'
Received message: ' any'
Received message: ' given'
Received message: ' time'
Received message: '.'
Received message: 'None'

Message is done!
Speaking: 'A woodchuck can only carry around one pound of food at any given time.'
Response was: A woodchuck can only carry around one pound of food at any given time.
```


## References

Most references are included in the script, but also see:

* [Docker Container Audio](https://leimao.github.io/blog/Docker-Container-Audio/) (how to allow the docker container to see the audio device)
