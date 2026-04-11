# Plex Media Exporter

Connects to a Plex server using the `plexapi` library and exports the entire movie and TV show library to a CSV file, named after the selected library. Runs from the terminal — pulls metadata (title, year, genre, rating, runtime) and saves everything into a clean CSV file.

## Requirements

- Python 3.x
- plexapi
- requests

## Installation

Clone the repo:
```bash
git clone https://github.com/zoltanlederer/plex-media-exporter.git
cd plex-media-exporter
```

Install dependencies:
```bash
pip install plexapi requests
```

Rename `config.example.py` to `config.py` and add your Plex URL and token:
```python
PLEX_URL = "http://localhost:32400" # or your server's IP (e.g. http://192.168.1.100:32400)
PLEX_TOKEN = "YOUR_TOKEN_HERE"
```

## Usage
```bash
python3 plex_exporter.py
```

## Example
```bash
python3 plex_exporter.py
======================================================================
Plex Media Exporter
Exports your Plex movie and TV show libraries to a CSV file.
Note: Music and photo libraries are not supported.
======================================================================
------------------------------
1: Movies
------------------------------
2: TV Shows
------------------------------
3: Music
------------------------------
4: Photos
----------------------------------------------------------------------
Type a number to select, or 'q' to quit: 1
----------------------------------------------------------------------
Exporting... 2962/2962
----------------------------------------------------------------------
Export complete. 2962 items saved to Movies.csv.
----------------------------------------------------------------------
```


## Tips

### How to find your Plex token
1. Open Plex in your browser
2. Play any movie or click into any media item
3. Click the three dots (···) menu
4. Click "Get Info"
5. At the bottom of that window, click "View XML"
6. A new tab opens with a long URL — look for `X-Plex-Token=` in that URL
7. Copy everything after the `=` sign — that's your token