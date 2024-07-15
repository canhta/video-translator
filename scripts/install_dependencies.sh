#!/bin/bash

# Check if Poetry is installed
if ! command -v poetry &> /dev/null
then
    echo "Poetry is not installed. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Install project dependencies
echo "Installing project dependencies..."
poetry install

# Install ffmpeg if not already installed
if ! command -v ffmpeg &> /dev/null
then
    echo "ffmpeg is not installed. Installing ffmpeg..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install ffmpeg
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt-get update
        sudo apt-get install -y ffmpeg
    else
        echo "Operating system not supported. Please install ffmpeg manually."
    fi
fi

echo "Installation complete!"
