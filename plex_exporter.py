"""
Plex Media Exporter

Connects to a Plex server using the plexapi library and exports the entire movie and TV show library to a CSV file. Runs from the terminal — pulls metadata (title, year, genre, rating, runtime) and saves everything into a clean CSV file.
"""

from plexapi.server import PlexServer
from config import PLEX_URL, PLEX_TOKEN

# Connect to the Plex server using URL and token from config.py
plex = PlexServer(PLEX_URL, PLEX_TOKEN)

# List all libraries to confirm the connection works
for library in plex.library.sections():
    print(library.title, library.type)

