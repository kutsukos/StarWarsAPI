# StarWarsAPI
A Python3 script that displays Star Wars characters' info, using The Star Wars API (swapi.tech), if info are not found in cache files


## Operations
This script supports 3 operations. search, clean_cache and statistics.

### Search
Searches Star Wars API for a character by name, if not found in cache files
<br>Search operation requires `--name` argument. With `--name` argument, you can define the character to be searched
<br>`--world` option is optional and if exists, the script displays character's homeworld information
<br> Usage example: `python3 starwars.py search --name OB --world` or `python3 starwars.py search --name 'luke sky'`
<br> Example output:
```
python3 starwars.py search --name 'luke sky'
Name: Luke Skywalker
Height: 172
Mass: 77
Birth Year: 19BBY

Cache time: 2023-04-10 16:04:55.824554

```
### Clean_cache
Cleans/removes the files, holding cache information
<br> Usage example: `python3 starwars.py clean_cache`

### Statistics
Prints on the terminal couple of statistics, related to this search script. Prints the hours in day this script is used, the number of times a search was successfull, the number of times each character was searched, etc.
<br> Usage example: `python3 starwars.py statistics`
<br> Example output:
```
* Hours and frequency of searches
16: 5 (100.00%)

* Stats related to Characters
Character Obi-Wan Kenobi was searched 2 time(s)
Character Luke Skywalker was searched 3 time(s)

* Stats related to Planets
Planet Stewjon was searched 1 time(s)
Planet Tatooine was searched 1 time(s)

* Generic Stats
We had 5/5 successful searche(s)
```

## Help
Run `python3 starwars.py --help`, to see the help message
