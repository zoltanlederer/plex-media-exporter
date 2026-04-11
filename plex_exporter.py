"""
Plex Media Exporter

Connects to a Plex server using the plexapi library and exports the entire movie and TV show library to a CSV file. Runs from the terminal — pulls metadata (title, year, genre, rating, runtime) and saves everything into a clean CSV file.
"""

import sys
import os
import csv
import requests
from plexapi.server import PlexServer
from config import PLEX_URL, PLEX_TOKEN


# Connect to the Plex server using URL and token from config.py
try:
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
except requests.exceptions.ConnectionError:
    print('Could not connect to Plex. Check your URL and token in config.py.')
    sys.exit()
except requests.exceptions.Timeout:
    print('Request timed out.')
    sys.exit()
except Exception:
    print('Something went wrong, please try again.')
    sys.exit()    

print("=" * 70)
print("Plex Media Exporter")
print("Exports your Plex movie and TV show libraries to a CSV file.")
print("Note: Music and photo libraries are not supported.")
print("=" * 70)

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
            print("-" * 70)
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


def collect_media(all_items, selected_type, total):
    """ Collects the media information from the selected library """
    media_list = [] # Store all media items
    
    # Add all media details to a list of dictionaries
    for index, item in enumerate(all_items, start=1):
        item_data = {
            'title': item.title,
            'titleSort': item.titleSort,
            'year': item.year,
            'genres': get_genres(item.genres),
            'duration': item.duration // 60000 if item.duration else None,
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

        # Progress indicator while collecting data
        # \r moves the cursor back to the start of the line
        # end='' prevents a new line being printed
        # flush=True forces it to display immediately
        print(f"\rExporting... {index}/{total}", end='', flush=True)
    print()  # move to next line after progress is done
    
    return media_list


def get_filename(selected_title):
    """ Check if the filename already exists and return the final filename """
    filename = f"{selected_title}.csv"
    while True:
        if os.path.exists(filename):
            print(f"-" * 70)
            new_filename = input(f'The "{filename}" already exists. Press "Enter" to overwrite, type a new name, or "q" to quit: ')
            if new_filename == 'q':  # file exists, user quit the program
                sys.exit()
            elif new_filename != '':  # file exists, user types a new name, loop again to recheck
                filename = f"{new_filename}.csv"
            else:  # file exists, user confirmed overwrite
                break
        else:
            break  # file doesn't exist, continue
    return filename


def export_to_csv(media_list, filename, selected_type):
    """ Write collected media data to CSV """
    try:
        with open(f"{filename}", 'w', newline='') as csvfile: # handles closing the file automatically    
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
    except PermissionError:
        print(f'Permission denied. Could not write to "{filename}".')
        sys.exit()
    except OSError as error:
        print(f'Could not create file: {error}')
        sys.exit()
    except Exception:
        print('Something went wrong while writing the file.')
        sys.exit()

    print("-" * 70)
    print(f"Export complete. {len(media_list)} items saved to {filename}.")
    print("-" * 70)


# List and select library
libraries = list_libraries(plex)
selected_library = library_confirmation(libraries)
selected_title = selected_library['library_title']
selected_type = selected_library['library_type']

# Fetch all items from the selected library
media = plex.library.section(selected_title)
all_items = media.all()
total = len(all_items)

# Collect, export
media_list = collect_media(all_items, selected_type, total)
filename = get_filename(selected_title)
export_to_csv(media_list, filename, selected_type)