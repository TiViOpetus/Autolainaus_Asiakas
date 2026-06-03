import json
import requests


class PaikanninDotCom:

    # Konstruktori
    def __init__(self, apikey, baseurl):
        """Creates an object for getting spatial data from paikannin.com

        Args:
            apikey (str): API-key to access paikannin.com
            baseurl (str): URL for API calls without parameters
        """
        self.apikey = apikey
        self.baseurl = baseurl

    def getVehicleIds(self):
        pass

    def getLocationNow(self, deviceId):
        pass

    def getNoPointsRoutes(self, deviceId, startTime, endTime):
        """ Loads trip addresses from paikannin.com for a vehicle at a given time

        Args:
            deviceId (int): vehicle's device number
            startTime (str): timestamp of drive started
            endTime (str): timestamp of drive ended

        Returns:
            list: list of dictionary entries containing starting and ending places of trip legs
        """
        # Define URL for API call
        # 'https://app.paikannin.com/public/api/devices/routes/nopoints/'
        methodUrl = f'{self.baseurl}/devices/routes/nopoints/'
        extension = f'{deviceId}/{startTime}/{endTime}'
        url = methodUrl + extension

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
        else:
            resultSet = []        
        
        return resultSet
    
    
if __name__ == "__main__":
    apiKey = ''
    baseurl = 'https://app.paikannin.com/public/api'
    deviceId = 104619
    startTime = '2026-03-22T08:00:00Z'
    endTime = '2026-03-27T10:00:00Z'
    paikanninDotCom = PaikanninDotCom(apiKey,baseurl)
    data = paikanninDotCom.getNoPointsRoutes(deviceId, startTime, endTime)
    print(data)