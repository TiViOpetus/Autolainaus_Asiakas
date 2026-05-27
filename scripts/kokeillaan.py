import json
import os
import sys

projectRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if projectRoot not in sys.path:
    sys.path.insert(0, projectRoot)

from lendingModules import dbOperations
from lendingModules import cipher
import requests


def extract_latest_trip_payload(location_data):
    """Returns the most relevant trip payload from common API wrapper structures."""
    payload = location_data

    if isinstance(payload, list):
        for item in reversed(payload):
            if isinstance(item, dict):
                return item
        return payload[-1] if payload else payload

    if isinstance(payload, dict):
        candidate_keys = (
            'routes',
            'trips',
            'data',
            'items',
            'results',
            'payload',
            'history',
        )

        for key in candidate_keys:
            nested_value = payload.get(key)
            if isinstance(nested_value, list) and nested_value:
                for item in reversed(nested_value):
                    if isinstance(item, dict):
                        return item
                return nested_value[-1]
            if isinstance(nested_value, dict):
                return nested_value

    return payload


def find_nested_value(payload, target_key):
    """Finds the first matching key in nested dict/list structures."""
    if isinstance(payload, dict):
        if target_key in payload:
            return payload[target_key]

        for value in payload.values():
            nested_value = find_nested_value(value, target_key)
            if nested_value is not None:
                return nested_value

    if isinstance(payload, list):
        for item in payload:
            nested_value = find_nested_value(item, target_key)
            if nested_value is not None:
                return nested_value

    return None


def normalize_trip_payload(payload):
    """Maps external JSON keys to one predictable internal structure."""
    if not isinstance(payload, dict):
        return payload

    route_start_source = find_nested_value(payload, 'routeStartPosition')
    route_stop_source = find_nested_value(payload, 'routeStopPosition')

    if route_start_source is None:
        route_start_source = payload

    if route_stop_source is None:
        route_stop_source = payload

    if isinstance(route_start_source, list):
        route_start_source = route_start_source[-1] if route_start_source else None
    if isinstance(route_stop_source, list):
        route_stop_source = route_stop_source[-1] if route_stop_source else None

    if not isinstance(route_start_source, dict):
        route_start_source = {}
    if not isinstance(route_stop_source, dict):
        route_stop_source = {}

    def pick_position_value(position_data, *keys):
        for key in keys:
            value = position_data.get(key)
            if value is not None and value != '':
                return value
        return None

    route_start_position = {
        'city': pick_position_value(route_start_source, 'city'),
        'houseno': pick_position_value(route_start_source, 'houseno'),
        'street': pick_position_value(route_start_source, 'street'),
    }

    route_stop_position = {
        'city': pick_position_value(route_stop_source, 'city'),
        'houseno': pick_position_value(route_stop_source, 'houseno'),
        'street': pick_position_value(route_stop_source, 'street'),
    }

    drive_start_odo = payload.get('driveStartOdo'),
    drive_stop_odo = payload.get('driveStopOdo'),

    return {
        'routeStartPosition': route_start_position,
        'routeStopPosition': route_stop_position,
        'driveStartOdo': drive_start_odo,
        'driveStopOdo': drive_stop_odo,
    }


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
    registerNumber = 'FNK-129'

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
    dbConnection5 = dbOperations.DbConnection(dbSettings)
    apiKey = currentSettings['paikanninApiKey']

    deviceId = 104619
    startTime = '2026-04-29T08:00:00Z'
    endTime = '2026-05-06T23:00:00Z'
    

    # Define URL for API call
    baseurl = f'https://app.paikannin.com/public/api/devices/routes/nopoints/'
    extension = f'{deviceId}/{startTime}/{endTime}'
    url = baseurl + extension

    headersApi = f'{apiKey}'
    headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "API_KEY": headersApi
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    responseData = response.json()
    latestTrip = extract_latest_trip_payload(responseData)
    normalizedTrip = normalize_trip_payload(latestTrip)

    print('Raw JSON:')
    print(json.dumps(responseData, ensure_ascii=False, indent=2))
    print('Normalized trip JSON:')
    print(json.dumps(normalizedTrip, ensure_ascii=False, indent=2))
    # Yritetään tallentaa normalisoitu sijaintidata web_paikkatieto-tauluun
    try:
        # Hae auki oleva lainausnumero rekisterinumerolla
        loan_number = dbConnection5.getActiveLoanNumberForReturn(registerNumber)
        print('Resolved loan_number:', loan_number)
        # If no loan number found, try a direct query for debugging
        if loan_number is None:
            try:
                rows = dbConnection5.filterColumsFromTable('lainaus', ['lainausnumero','rekisterinumero','palautusaika'], f"rekisterinumero = '{registerNumber}' AND palautusaika IS NULL")
                print('Direct query for open loans returned:', rows)
            except Exception as qerr:
                print('Direct loan query failed:', qerr)
            # Try to fallback to the most recent loan even if it's closed
            latest = dbConnection5.getLatestLoanNumberForRegistration(registerNumber)
            print('Fallback latest loan number (may be closed):', latest)
            if latest is not None:
                loan_number = latest

        save_result = dbConnection5.saveWebPaikkatietoData(registerNumber, loan_number, normalizedTrip)
        print('saveWebPaikkatietoData returned:', save_result)
    except Exception as err:
        print('Error saving to web_paikkatieto:', err)


saveReturnData()