import json
import requests


class PaikanninDotCom:

    # Konstruktori
    def __init__(self, apikey, baseurl):
        self.apikey = apikey
        self.baseurl = baseurl

    def getVehicleIds(self):
        pass

    def getLocationNow(self, deviceId):
        pass

    def getNoPointsRoutes(self, deviceId, startTime, endTime):

        # Define URL for API call
        baseurl = f'https://app.paikannin.com/public/api/devices/routes/nopoints/'
        extension = f'{deviceId}/{startTime}/{endTime}'
        url = baseurl + extension

        # Define header and set an empty payload
        payload = ""
        headersApi = f'{self.apikey}'
        headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "EchoapiRuntime/1.1.0",
        "Connection": "keep-alive",
        "API_KEY": headersApi
        }

        # Get a response from paikannim.com using API
        response = requests.request("GET", url, data=payload, headers=headers)
        
        responseStatus = str(response.status_code)

        if responseStatus == '200':
            # Convert response to python format
            responseData = response.text
            spatialData = json.loads(responseData)
            resultSet = []

            # Loop spatial data to get route legs, odometer values and places
            for spatialDataRow in spatialData:
                startOdo = round(spatialDataRow['driveStartOdo'] / 1000)
                stopOdo = round(spatialDataRow['driveStopOdo'] / 1000)
                startPlace = spatialDataRow['routeStartPosition']
                stopPlace = spatialDataRow['routeStopPosition']

                # Create fields for inserting into a database
                fromFieldText = f"'{startPlace['street']} {startPlace['houseno']} {startPlace['city']}'"
                toFieldText = f"'{stopPlace['street']} {stopPlace['houseno']} {stopPlace['city']}'"
                resultSet.append({'fromField': fromFieldText, 'toField': toFieldText, 'startOdo': startOdo, 'stopOdo': stopOdo})
                
        print(resultSet)
        return resultSet
    



    