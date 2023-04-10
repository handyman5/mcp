# MCP

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

## References

Most references are included in the script, but also see:

* [Docker Container Audio](https://leimao.github.io/blog/Docker-Container-Audio/) (how to allow the docker container to see the audio device)
