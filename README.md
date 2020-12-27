![Test](https://github.com/ThorsHamster/find_new_hometown/workflows/Test/badge.svg)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4c8fdd5fca7c49cb9c21eac099af97ce)](https://www.codacy.com/manual/ThorsHamster/find_new_hometown?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ThorsHamster/find_new_hometown&amp;utm_campaign=Badge_Grade)
[![CodeFactor](https://www.codefactor.io/repository/github/thorshamster/find_new_hometown/badge?s=490599446953487415bc297769f782570860b96c)](https://www.codefactor.io/repository/github/thorshamster/find_new_hometown)

# find_new_hometown

A project to find a new home town. 
Both partners want to have approximately the same distance or duration to their workplace. 
This project aims to find the best place to live with the shortest possible distance or duration for both partners.

**Note**: In this repo my personal encrypted settings.yml, cities.yml and data.db are checked in. 
You have to delete them and use your own.

## Settings

A openrouteservice api key is needed ([openrouteservice](https://openrouteservice.org/dev/#/login)).

**Note**: openrouteservice has some limitations regarding query speed and frequency.
Maybe it is necessary to download all data in several sessions, depending on the amount of cities.
For every city one request for *GeocodeSearch* and two requests for *Matrix V2* (distance and duration) are necessary.

Furthermore you have to specify all necessary data in: **settings.yml**:

Like the openroutservice api key and the two working places.
The **option** must also be specified whether to optimize by *duration* or *distance*.
```yaml
api_key: _insert_your_personal_api_key_here_
target_city_1: _Working_place_of_partner_1_  # e.g. 38350 Helmstedt
target_city_2: _Working_place_of_partner_2_  # e.g. Magdeburg
option: duration
``` 

Also a list of cities to investigate is needed: **cities.yml**:
```yaml
# taken from https://de.wikipedia.org/wiki/Liste_der_St%C3%A4dte_und_Gemeinden_in_Sachsen-Anhalt
cities:
 - Altenhausen, Börde, Sachsen-Anhalt
 - Am Großen Bruch, Börde, Sachsen-Anhalt
 - Angern, Börde, Sachsen-Anhalt
 - Ausleben, Börde, Sachsen-Anhalt
 - Barleben, Börde, Sachsen-Anhalt
 - Beendorf, Börde, Sachsen-Anhalt
 - Bülstringen, Börde, Sachsen-Anhalt
 - Burgstall, Börde, Sachsen-Anhalt
 - ...
``` 

**Note**: If a city has a name that occurs frequently, 
it is recommended to add the postal code to get a unique name. 
Also the indication of the district is helpful.
You can get a list of all towns in a district on e.g. Wikipedia.

**How to use it**:
If all necessary information is given, like *cities.yml* and *settings.yml*, 
and all required packages are installed, just use it as follows:
```python
python main.py
```
or use a IDE like PyCharm.

## Output

![Example Output](https://user-images.githubusercontent.com/48162347/71783309-51866580-2fe5-11ea-894a-9e8b5ec13928.png)

A html page will be created with a world map and all given cities. 
The two workplaces are marked as blue dots. 
All other cities are shown either as red, yellow or green points.
Cities closest to the middle of the route are marked green, cities further 
away are marked yellow and cities that are only convenient for one 
of the two partners are marked red.

Example Output: The higher the city is in the list (the smaller the number), the more likely it is that 
the city at the centre of the two workplaces.

```bash
Altenhausen, Börde, Sachsen-Anhalt                0.20
Erxleben, Börde, Sachsen-Anhalt                   0.20
Eilsleben, Börde, Sachsen-Anhalt                  2.81
Calvörde, Börde, Sachsen-Anhalt                   5.50
Ausleben, Börde, Sachsen-Anhalt                   6.60
Westheide, Börde, Sachsen-Anhalt                  6.93
Ummendorf, Börde, Sachsen-Anhalt                  7.84
Ingersleben, Börde, Sachsen-Anhalt                9.96
Am Großen Bruch, Börde, Sachsen-Anhalt           11.88
...
```

## Prerequisitions
-   openrouteservice api key: [openrouteservice](https://openrouteservice.org/dev/#/login)
-   python 3
-   see [requirements.txt](https://github.com/ThorsHamster/find_new_hometown/blob/master/requirements.txt)
