import requests
import os.path as io
import time
from datetime import date, timedelta
from colorama import Fore, Style

# Intro
print("--=[ PolenPy by Cysecor ]=--")
time.sleep(1)
print("--=[ Skripta pokazuje koncentraciju polena u izabranom mjestu u poslednjih X dana. ]=--")
time.sleep(3)

print(Fore.GREEN)
# Broj dana za prikaz.
days_num = input("Unesi broj dana: ")
print(Style.RESET_ALL)

# Uzimamo danasnji datum.
today = date.today()
# Kalkulacija datuma.
new_date = today - timedelta(4 + int(days_num))
# Adaptiranje datuma za potrebni format.
starting_date = new_date.strftime("%Y-%m-%d")


# Ako fajl ne postoji kreiraj ga i popuni podacima.
# Ovo se radi da ne bi svaki put kada pokrenemo program pozivali API bez potrebe.
if not io.isfile("locations.txt"):
    # Pozivanje API-ja da dobijemo listu mjesta u Srbiji.
    locations_list = requests.get("http://polen.sepa.gov.rs/api/opendata/locations/")

    # Dodjeljivanje JSON podataka varijabli (lista).
    locations_list = locations_list.json()

    # Sortiranje liste po ID-u.
    locations_list = sorted(locations_list, key=lambda k: k['id'])

    # Otvaramo fajl da popunimo podatke.
    file = open("locations.txt", "w")

    # Petljom vrtimo kroz listu i upisujemo sve u fajl.
    for item in locations_list:
        file.write(f"{item['id']}: {item['name']} - {item['description']}\n")

    # Po zavrsenom poslu, obavezno zatvoriti fajl.
    file.close()

# Citanje fajla kako bi uzeli podatke o mjestima.
locations = open("locations.txt", "r")
for line in locations:
    print(line, end='')

# Zatvaramo fajl.
locations.close()

print(Fore.GREEN)
# Pitamo korisnika da unese mjesto.
location = input("Unesi mjesto (broj): ")
print(Style.RESET_ALL)

# Pozivamo API da dobijemo podatke o polenu za uneseno mjesto i datum.
pollen = requests.get(f"http://polen.sepa.gov.rs/api/opendata/pollens/?date_after={starting_date}&location={location}")
pollen = pollen.json()

# Uzimamo bitne podatke iz JSONa.
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
            print(f"Koncentracija polena {allergen['localized_name']} ({allergen['name']}) visoka!!!")
        elif allergen['margine_top'] >= current_value >= allergen['margine_bottom']:
            print(f"Koncentracija polena {allergen['localized_name']} ({allergen['name']}) srednja!")
        else:
            print(f"Koncentracija polena {allergen['localized_name']} ({allergen['name']}) mala.")

    print("\n================================================\n")