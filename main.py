import requests
import os.path as io
from datetime import date, timedelta
import time
from colorama import Fore, Style

print("--=[ PolenPy by Cysecor ]=--")
time.sleep(1)
print("--=[ Skripta pokazuje koncentraciju polena u izabranom mjestu u poslednjih X dana. ]=--")
time.sleep(3)

print(Fore.GREEN)
days_num = input("Unesi broj dana: ")
print(Style.RESET_ALL)

today = date.today()

starting_date = today - timedelta(4 + int(days_num))

if not io.isfile("locations.txt"):
    file = open("locations.txt", "w")

    locations_list = requests.get("http://polen.sepa.gov.rs/api/opendata/locations/")
    locations_list = locations_list.json()

    locations_list = sorted(locations_list, key=lambda k: k['id'])

    for item in locations_list:
        file.write(f"{item['id']}: {item['name']} - {item['description']}\n")

    file.close()

locations = open("locations.txt", "r")
for line in locations:
    print(line, end='')

locations.close()

print(Fore.GREEN)
location = input("Unesi mjesto (broj): ")
print(Style.RESET_ALL)

pollen = requests.get(f"http://polen.sepa.gov.rs/api/opendata/pollens/?location={location}&date_after={starting_date}")
pollen = pollen.json()

pollen = pollen['results']

print("================================================\n")

for item in pollen:
    print(f"Za dan: {Fore.BLUE}{item['date']}{Style.RESET_ALL}")

    for inner_item in item['concentrations']:
        concentrations = requests.get(f"http://polen.sepa.gov.rs/api/opendata/concentrations/{inner_item}")
        concentrations = concentrations.json()

        allergen = requests.get(f"http://polen.sepa.gov.rs/api/opendata/allergens/{concentrations['allergen']}")
        allergen = allergen.json()

        current_value = concentrations['value']

        if current_value > allergen['margine_top']:
            print(f"Koncentracija polena {allergen['localized_name']} ({allergen['name']}) je visoka!!!")
        elif allergen['margine_top'] >= current_value >= allergen['margine_bottom']:
            print(f"Koncentracija polena {allergen['localized_name']} ({allergen['name']}) je srednja!")
        else:
            print(f"Koncentracija polena {allergen['localized_name']} ({allergen['name']}) je niska.")

    print("\n================================================\n")