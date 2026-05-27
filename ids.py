import json

# Avataan tiedosto ja muutetaan se python-muotoon
with open('KaikkiAutot.json', 'rt') as autoala: # with sulkee tiedoston automaattisesti

    jsonData = autoala.read()
    parsedAutoData = json.loads(jsonData)

for vehicle in parsedAutoData:
    data = f"Rekisterinumero: {vehicle['name']} id: {vehicle['id']}"
    print(data)

