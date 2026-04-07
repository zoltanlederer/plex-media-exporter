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
    # print(library.title, library.type)


def list_libraries(plex):
    """ Fetch and display all Plex libraries, and return them as a list of dictionaries """
    libraries = list()
    # enumerate() gives the number and the item at the same time
    for index, library in enumerate(plex.library.sections(), start=1):
        print("-" * 30)
        print(f"{index}: {library.title}")
        libraries.append({'library_number': index, 'library_title': library.title})
    return libraries

def library_confirmation(libraries):
    """ Display a prompt for the user to select a library and return the selected library name """
    print("-" * 70)
    selected_library = int(input('Select a library (enter the number): '))
    selected_library = libraries[selected_library-1]['library_title']
    # print(selected_library)
    return selected_library

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


libraries = list_libraries(plex)
selected_library = library_confirmation(libraries)

list_of_movies = []

# Access the selected library
movies = plex.library.section(selected_library)

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
