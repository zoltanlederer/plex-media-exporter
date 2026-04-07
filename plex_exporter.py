"""
Plex Media Exporter

Connects to a Plex server using the plexapi library and exports the entire movie and TV show library to a CSV file. Runs from the terminal — pulls metadata (title, year, genre, rating, runtime) and saves everything into a clean CSV file.
"""

import csv
from plexapi.server import PlexServer
from config import PLEX_URL, PLEX_TOKEN

# Connect to the Plex server using URL and token from config.py
plex = PlexServer(PLEX_URL, PLEX_TOKEN)

# FOR REFERENCE: List all libraries to confirm the connection works
# for library in plex.library.sections():
#     print(library.title, library.type)

def get_guid(guid, provider):
    """ Extract the external ID for a given provider (imdb, tmdb) """
    for ids in guid:
        if ids.id.startswith(f'{provider}://'):
            return ids.id.replace(f'{provider}://', '')
    return None


def get_genres(genres):
    """ Extract the genre names from Genre objects as a comma-separated string """
    all_genres = []
    for genre in genres:
        all_genres.append(genre.tag)
    return ', '.join(all_genres)


list_of_movies = []

# Access the movies library (Filmek)
movies = plex.library.section('Filmek')

# Add all movie details to a list of dictionaries
for movie in movies.all():
    list_of_movies.append({'title': movie.title, 'titleSort': movie.titleSort, 'year': movie.year, 'rating': movie.rating, 'genres': get_genres(movie.genres), 'duration': movie.duration // 60000, 'studio': movie.studio, 'tagline': movie.tagline, 'summary': movie.summary, 'originallyAvailableAt': movie.originallyAvailableAt, 'imdb_id': get_guid(movie.guids, 'imdb'), 'tmdb_id': get_guid(movie.guids, 'tmdb')}) 

print(list_of_movies)

# Write collected movie data to CSV
with open('export.csv', 'w', newline='') as csvfile: # with open(...) — handles closing the file automatically    
    fieldnames = ['title','titleSort','year','rating','genres','duration','studio','tagline','summary','originallyAvailableAt','imdb_id','tmdb_id'] # defines the column headers, and the order they appear in the CSV
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader() # writes the first row with column names
    writer.writerows(list_of_movies) # writes all the dictionaries in one go
