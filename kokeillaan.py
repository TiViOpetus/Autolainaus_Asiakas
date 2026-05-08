from lendingModules import dbOperations
from lendingModules import cipher
import requests
import json


# Rutiini, joka lukee asetukset, jos ne ovat olemassa
try:
    # Avataam asetustiedosto ja muutetaan se Python sanakirjaksi
    with open('settings.json', 'rt') as settingsFile: # With sulkee tiedoston automaattisesti
        
        jsonData = settingsFile.read()
        currentSettings = json.loads(jsonData)
    
    # Puretaan salasana tietokantaoperaatioita varten  
    plainTextPassword = cipher.decryptString(currentSettings['password'])

    print('Salasana on selväkielisenä', plainTextPassword)
        
# Jos asetusten luku ei onnistu, näytetäänvirheilmoitus
except Exception as error:
    title = 'Tietokanta-asetusten luku ei onnistunut'
    text = 'Tietokanta-asetuksien avaaminen ja salasanan purku ei onnistunut'
    print(title)
    

def saveReturnData():
    
    dbSettings = currentSettings
    dbSettings['password'] = plainTextPassword # Vaihdetaan selväkieliseksi
    dbConnection = dbOperations.DbConnection(dbSettings)
    registerNumber = f"'FNK-129'" # Tekstiä -> lisää ':t

    # dbConnection.updateReturnTimeStamp('lainaus', 'palautusaika', 'rekisterinumero', criteria)
    
    # Haetaan palautettavan auton lainausnumero
    #lendingId = dbConnection.getNotReturnedId(registerNumber)

    """  # Päivitetään palautuksen ajankohta
    dbConnection2 = dbOperations.DbConnection(dbSettings)
    dbConnection2.setReturnTimestamp(lendingId)

    # Haetaan aloitus ja päättymisaika lainauksesta
    # Päivitetään palautuksen ajankohta
    dbConnection3 = dbOperations.DbConnection(dbSettings)
    timeStamps = dbConnection3.getTimestamps(lendingId)
    startTime = timeStamps[0]
    endTime = timeStamps[1]

    # Haetaan auton paikannin.com:n laitetunnus
    dbConnection4 = dbOperations.DbConnection(dbSettings)
    deviceId = dbConnection4.getDeviceId(registerNumber) """

    # Haetaan paikannin.com:n API-avain tietokannasta
    print(dbSettings)
    dbConnection5 = dbOperations.DbConnection(dbSettings)
    apiKey = dbConnection5.getSettingsValue('paikkatietoAPI')
    print('API:n pituus on', len(apiKey))

    deviceId = 104619
    startTime = '2026-03-22T08:00:00Z'
    endTime = '2026-03-27T10:00:00Z'
    

    # Define URL for API call
    baseurl = f'https://app.paikannin.com/public/api/devices/routes/nopoints/'
    extension = f'{deviceId}/{startTime}/{endTime}'
    url = baseurl + extension

    # Define header and set an empty payload
    payload = ""
    headersApi = f'{apiKey}'
    headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "EchoapiRuntime/1.1.0",
    "Connection": "keep-alive",
    "API_KEY": headersApi
    }


    # Get a response from paikannim.com using API
    response = requests.request("GET", url, data=payload, headers=headers)
    

    # Convert responset to python format
    responseData = response.text
    spatialData = json.loads(responseData)
    
    # Loop spatial data to get route legs, odometer values and places
    for spatialDataRow in spatialData:
        startOdo = round(spatialDataRow['driveStartOdo'] / 1000)
        stopOdo = round(spatialDataRow['driveStopOdo'] / 1000)
        startPlace = spatialDataRow['routeStartPosition']
        stopPlace = spatialDataRow['routeStopPosition']

        a_kaupunki = startPlace['city']
        a_katu = startPlace['street']
        a_katunumero = startPlace['houseno']


        b_kaupunki = stopPlace['city']
        b_katu = stopPlace['street']
        b_katunumero = stopPlace['houseno']

        print('Mistä', startPlace, startOdo)
        print('Mihin', stopPlace, stopOdo)
        

saveReturnData()

       