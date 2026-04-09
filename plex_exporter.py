"""
Plex Media Exporter

Connects to a Plex server using the plexapi library and exports the entire movie and TV show library to a CSV file. Runs from the terminal — pulls metadata (title, year, genre, rating, runtime) and saves everything into a clean CSV file.
"""

import sys
import csv
from plexapi.server import PlexServer
from config import PLEX_URL, PLEX_TOKEN

# Connect to the Plex server using URL and token from config.py
plex = PlexServer(PLEX_URL, PLEX_TOKEN)

# FOR REFERENCE: List all libraries to confirm the connection works
# for library in plex.library.sections():
#     print(library.title, library.type)


def list_libraries(plex):
    """ Fetch and display all Plex libraries, and return them as a list of dictionaries """
    libraries = list()
    # enumerate() gives the number and the item at the same time
    for index, library in enumerate(plex.library.sections(), start=1):
        print("-" * 30)
        print(f"{index}: {library.title}")
        libraries.append({'library_number': index, 'library_title': library.title, 'library_type': library.type})
    return libraries


def library_confirmation(libraries):
    """ Display a prompt for the user to select a library and return the selected library name """
    print("-" * 70)
    while True:  # keep asking until valid input is received
        try:
            number = input("Type a number to select, or 'q' to quit: ")
            if number == 'q':
                sys.exit()
            
            number = int(number)
            if 1 <= number <= len(libraries):  # check if number is within valid range
                return libraries[number - 1]  # return the full library dictionary
            else:
                print(f'Please enter a number between 1 and {len(libraries)}.')
        except ValueError:  # int() raises ValueError if the input is not a number
            print('Invalid input. Please enter a number.')


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
selected_title = selected_library['library_title']
selected_type = selected_library['library_type']

# Store all media items
media_list = []

# Access the selected library
media = plex.library.section(selected_title)

# Add all media details to a list of dictionaries
for item in media.all():
    item_data = {
        'title': item.title,
        'titleSort': item.titleSort,
        'year': item.year,
        'genres': get_genres(item.genres),
        'duration': item.duration // 60000,
        'studio': item.studio,
        'tagline': item.tagline,
        'summary': item.summary,
        'originallyAvailableAt': item.originallyAvailableAt.strftime('%Y-%m-%d') if item.originallyAvailableAt else None,
        'imdb_id': get_guid(item.guids, 'imdb'),
        'tmdb_id': get_guid(item.guids, 'tmdb')
    }

    if selected_type == 'show':
        item_data['seasonCount'] = item.seasonCount
        item_data['leafCount'] = item.leafCount

    media_list.append(item_data) 


# Write collected media data to CSV
with open(f"{selected_title}.csv", 'w', newline='') as csvfile: # handles closing the file automatically    
    movie_fieldnames = [
        'title',
        'titleSort',
        'year',
        'genres',
        'duration',
        'studio',
        'tagline',
        'summary',
        'originallyAvailableAt',
        'imdb_id',
        'tmdb_id'
    ] # defines the column headers, and the order they appear in the CSV
    
    show_fieldnames = [
        'seasonCount',
        'leafCount',
    ] # defines the column headers, and the order they appear in the CSV
    
    if selected_type == 'show':
        fieldnames = movie_fieldnames + show_fieldnames
    else:
        fieldnames = movie_fieldnames

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader() # writes the first row with column names
    writer.writerows(media_list) # writes all the dictionaries in one go

