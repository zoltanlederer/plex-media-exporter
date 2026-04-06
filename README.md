# Plex Media Exporter

Connects to a Plex server using the `plexapi` library and exports the entire movie and TV show library to a CSV file. Runs from the terminal — pulls metadata (title, year, genre, rating, runtime) and saves everything into a clean CSV file.

## Requirements

- Python 3.x
- plexapi

## Setup

1. Clone the repo
2. Install dependencies: `pip install plexapi`
3. Add your Plex URL and token to `config.py`

## Usage
```bash
python plex_exporter.py
```