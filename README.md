# find_new_hometown

A project to find a new hometown to live in.
Both partners must travel to work by car. 
This project aims to find the best place to live with 
the shortest possible travel distance for both partners.

**Note**: In this repo my personal encrypted settings.yml, cities.yml and data.db are checked in. 
You have to delete them and use your own.

## Settings

A openrouteservice api key is needed ([openrouteservice](https://openrouteservice.org/dev/#/login)).

**Note**: openrouteservice has some limitations regarding query speed and frequency.
Maybe it is necessary to download all data in several sessions, depending on the amount of cities.
For every city one request for *GeocodeSearch* and two requests for *Matrix V2* (distance and duration) are necessary.

Furthermore you have to specify all necessary data in settings.yml:
```yaml
api_key: _insert_your_personal_api_key_here_
target_city_1: _Working_place_of_partner_1_  # e.g. Berlin
target_city_2: _Working_place_of_partner_2_  # e.g. Hannover
``` 

Also a list of cities to investigate is needed: cities.yml:
```yaml
cities:
  - Braunschweig
  - Wolfburg
  - Magdeburg
  - Brandenburg an der Havel
  - 38350 Helmstedt
  - 14641 Nauen, Havelland, Brandenburg
  - ...
``` 

**Note**: If a city has a name that occurs frequently, 
it is recommended to add the postal code to get a unique name. 
Also the indication of the district is helpful.

## Output

Example Output: The higher the city (smaller number), the more likely 
the city is to be in the centre of the two places of work.

```python
Magdeburg                               12.29
38350 Helmstedt                        116.83
Brandenburg an der Havel               127.82
Wolfsburg                              142.27
Braunschweig                           171.29
14641 Nauen, Havelland, Brandenburg    220.68
```

## Prerequisitions:
-   openrouteservice api key: [openrouteservice](https://openrouteservice.org/dev/#/login)
-   python 3
-   see [requirements.txt](https://github.com/ThorsHamster/find_new_hometown/blob/master/requirements.txt)