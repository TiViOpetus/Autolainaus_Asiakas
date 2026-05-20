import json

# Avataan tiedosto ja muutetaan se Python-muotoon
with open('KaikkiAutot.json', 'rt') as autodata: # With sulkee tiedoston automaattisesti
                
    jsonData = autodata.read()
    parsedAutoData = json.loads(jsonData)

for vehicle in parsedAutoData:
    data = f'Rekisterinumero: {vehicle['name']} id: {vehicle['id']}'
    print(data)
 
