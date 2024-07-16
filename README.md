# Video Translator

## Introduction

Video Translator is a library for processing videos and text.

## Getting Started

### Download Youtube Video

```sh
poetry run download [YOUTUBE_ID]

# or
youtube-dl -d [YOUTUBE_ID]
```

After that, the .webm video file will be downloaded in the `./output.[video title]` folder.

## Project Structure

```bash
video_translator/
│
├── pyproject.toml
├── poetry.lock
├── README.md
├── LICENSE
├── .gitignore
├── .pre-commit-config.yaml
│
├── src/
│   └── video_translator/
│       ├── __init__.py
│       ├── main.py
│       ├── audio_processor.py
│       ├── text_processor.py
│       ├── video_processor.py
│       └── utils.py
│
├── tests/
│   ├── __init__.py
│   ├── test_audio_processor.py
│   ├── test_text_processor.py
│   └── test_video_processor.py
│
└── docs/
    ├── conf.py
    └── index.rst
```
