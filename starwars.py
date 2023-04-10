import requests
import json
import argparse
from datetime import datetime
from collections import Counter
import os

# Variables
# Search endpoints for Star Wars characters and planets
CHARACTER_SEARCH_URL = 'https://swapi.tech/api/people/?name={}'
PLANET_GET_URL = 'https://www.swapi.tech/api/planets/{}'

# Filenames where cache dictionaries are saved
WORLD_CACHE_FILENAME = 'cache_world.json'
CHARACTER_CACHE_FILENAME = 'cache_character.json'
STATISTICS_FILENAME = 'cache_stats.json'

# Planet Earth variables
EARTH_ROTATION_PERIOD = 24
EARTH_ORBITAL_PERIOD = 365

# Methods
# This method removes the cache files if they exist
def clean_cache():
    # Cache for Worlds/Planets
    if (os.path.exists(WORLD_CACHE_FILENAME)):
      try:
        os.remove(WORLD_CACHE_FILENAME)
      except:
        print(f'Something went wrong on removal of file {WORLD_CACHE_FILENAME}')
    # Cache for Characters
    if (os.path.exists(CHARACTER_CACHE_FILENAME)):
      try:
        os.remove(CHARACTER_CACHE_FILENAME)
      except:
        print(f'Something went wrong on removal of file {CHARACTER_CACHE_FILENAME}')
    # Cache for Statistics
    if (os.path.exists(STATISTICS_FILENAME)):
      try:
        os.remove(STATISTICS_FILENAME)
      except:
        print(f'Something went wrong on removal of file {STATISTICS_FILENAME}')

# This method stores a dictionary to a file
def save_cache(cache, filename):
    try:
        json.dump(cache, open(filename, 'w'))
    except:
        print(f'Something went wrong on writing on file {filename}')

# This method reads a file and return the file's contents as dictionary
# If cannot open the file, returns an empty dictionary
# Used for the persistent cache functionality
def open_cache(filename):
    try:
        cache = json.load(open(filename, 'r'))
    except (IOError, ValueError):
        cache = {}
    return cache

# This method returns the current time
# Used for the persistent cache functionality
def get_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S.%f")

# This method gets and displays Star Wars character's homeworld information, 
# from cache file and if does not exist, gets this info from API and 
# stores it into the cache file for future use.
# If we get info from API, we save that info to the cache file too for future use
def get_characters_world(planet_number):

    # Read the cache file for Planets and save it into dictionary 'world_cache'
    world_cache = open_cache(WORLD_CACHE_FILENAME)

    # if we cannot find planet's info in the dictionary, we retrieve them from the API
    if planet_number not in world_cache:
        response  = requests.get(PLANET_GET_URL.format(planet_number))

        # If the request was successful, save the results to the dictionary, 
        # with the current time as cache time and 1 as the times searched
        if response.status_code == 200:
                world_cache[planet_number]= [response.json()['result'], get_time(), 1]
        else:
                print("The force is not strong within you. Cannot get information for planets from the API")
                return 0
    # if planet exists in dictionary, then increase the times it was searched
    else:
        world_cache[planet_number][2]+=1
    
    # save the dictionary with latest updates on cache file
    save_cache(world_cache, WORLD_CACHE_FILENAME)

    # Time to print the Planet's info
    planet = world_cache[planet_number][0]["properties"]

    planet_name = planet['name']
    planet_population = planet['population']
    rotation_period = planet['rotation_period']
    orbital_period = planet['orbital_period']

    print("\nHomeworld\n-------------")
    print(f'Name: {planet_name}')
    print(f'Population: {planet_population}')

    # if we have infos for planet's rotation, we can display these in comparison to earth's
    if rotation_period.isnumeric() and orbital_period.isnumeric():
        earth_planet_year = int(orbital_period)/EARTH_ORBITAL_PERIOD
        earth_planet_day = int(rotation_period)/EARTH_ROTATION_PERIOD
        print(f'On {planet_name}, 1 year on Earth is {earth_planet_year:.2f} years and 1 day {earth_planet_day:.2f} days')
    cache_time = world_cache[planet_number][1]
    print(f'\nCache time: {cache_time}')

    return 1

# This method searches for Star Wars characters by name in the cache file
# and if does not exist, gets this info from API and stores it into the cache file
# for future use.
# If character cannot be retrieved from API, an error message will be printed
def search_characters_by_name(name, world=0):

    # Read the cache file for Characters and save it into dictionary 'character_cache'
    character_cache = open_cache(CHARACTER_CACHE_FILENAME)

    # search name in character's dict
    # if we find someone's full name that matches user's input,
    # we keep the character's full-name
    for character_name in character_cache:
        if name.casefold() in character_name.casefold():
                name = character_name

    # if we cannot find character's info in the dictionary, we retrieve it from the API
    if name not in character_cache:
        response = requests.get(CHARACTER_SEARCH_URL.format(name))

        # If the request was successful, save the results to the dictionary, 
        # with the current time as cache time and 1 as the times searched
        if response.status_code == 200:
                results = response.json()["result"]
                # the response is ok, but we did not get any results
                if len(results) == 0 :
                        print("The force is not strong within you")
                        return 0
                name = results[0]["properties"]['name']
                character_cache[name] = [results[0], get_time(), 1]
        else:
                print("The force is not strong within you. Cannot get information for the character from the API")
                return 0
    # if character exists in dictionary, then increase the times it was searched
    else:
        character_cache[name][2]+=1
    
    # save the dictionary with latest updates on cache file
    save_cache(character_cache, CHARACTER_CACHE_FILENAME)

    # Time to print character's info
    character = character_cache[name][0]["properties"]
    character_name = character['name']
    character_height = character['height']
    character_mass = character['mass']
    character_birth_year = character['birth_year']
    character_planet_no = character['homeworld'].split('/')[-1]

    print(f'Name: {character_name}')
    print(f'Height: {character_height}')
    print(f'Mass: {character_mass}')
    print(f'Birth Year: {character_birth_year}')

    cache_time = character_cache[name][1]
    print(f'\nCache time: {cache_time}')

    if world != 0:
        return get_characters_world(character_planet_no)
    return 1

# This method keeps extra info for statistics. For now, we keep the hours people use this script
def keep_statistics():
    stats_cache = open_cache(STATISTICS_FILENAME)

    now = datetime.now()
    hour_of_operation = now.strftime("%H")

    if len(stats_cache) == 0:
        stats_cache["hours"] = [hour_of_operation]
    else:
        stats_cache["hours"].append(hour_of_operation)
    stats_cache["hours"].sort();
    save_cache(stats_cache, STATISTICS_FILENAME)

# This method prints on the terminal couple of statistics, related to this search script
def print_statistics():
    stats_cache = open_cache(STATISTICS_FILENAME)
    world_cache = open_cache(WORLD_CACHE_FILENAME)
    character_cache = open_cache(CHARACTER_CACHE_FILENAME)

    # check if we have anything to report
    if stats_cache == {}:
        print(f'No stats to report')
        return
    all_searches = len(stats_cache["hours"])

    print(f'* Hours and frequency of searches')
    search_freq_count = Counter(stats_cache["hours"])
    for item, times in search_freq_count.items():
        freq = (times/all_searches)*100
        print(f"{item}: {times} ({freq:.2f}%)")

    print(f'\n* Stats related to Characters')
    successful_character_searches = 0
    for character in character_cache:
        print(f'Character {character} was searched {character_cache[character][2]} time(s)')
        successful_character_searches += character_cache[character][2]
    
    print(f'\n* Stats related to Planets')
    for planet in world_cache:
        planet_name = world_cache[planet][0]["properties"]['name']
        print(f'Planet {planet_name} was searched {world_cache[planet][2]} time(s)')
    
    print(f'\n* Generic Stats')
    print(f'We had {successful_character_searches}/{all_searches} successful searche(s)')



# The main method
def main(operation, name, world=0):
        if operation == 'search' and name!='':
                search_characters_by_name(name, world)
                keep_statistics()
        elif operation == 'clean_cache':
                clean_cache()
        elif operation == 'statistics':
                print_statistics()
        else:
                print("This operation, I support not. May the force be with you!")
        

if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Script that displays Star Wars characters' info, using The Star Wars API (swapi.tech)")
        parser.add_argument('operation', choices=['search','clean_cache','statistics'], help='Operation to perform')
        parser.add_argument('--name', help="Input character's name for search",default='')
        parser.add_argument('--world', help="Display character's homeworld", action='store_true')
        args = parser.parse_args()
        main(args.operation, args.name, args.world)
