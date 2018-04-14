import json
import requests

# Class for fetching data from Socialstyrelsen's open data.
class SocRequest:

    # Returns average numbers of suicides per year per region
    # as a Dictionary of key-value pairs.
    def getSuicideDict(self):

        API_URL = 'http://sdb.socialstyrelsen.se/api/v1/sv/'
        REGION_STR = '1,3,4,5,6,7,8,9,10,12,13,14,' \
                '17,18,19,20,21,22,23,24,25'
        YEAR_STR = '2007,2008,2009,2010,2011,2012,2013,2014,2015,2016'
        antalAr = YEAR_STR.count(',') + 1

        requestURL = API_URL + 'dodsorsaker/resultat/matt/1'\
                + '/diagnos/2026/kon/3' \
                + '/region/' + REGION_STR\
                + '/ar/' + YEAR_STR

        response = requests.get(requestURL)
        suicideJson = response.json()

        if(response.status_code == 200):
            suicideDictData = suicideJson['data']

            totalRegionDict = {}
            for e in suicideDictData:
                if int(e['regionId']) in totalRegionDict:
                    totalRegionDict[int(e['regionId'])] += int(e['varde'])
                else:
                    totalRegionDict[int(e['regionId'])] = int(e['varde'])

            for key in totalRegionDict:
                totalRegionDict[key] = round(totalRegionDict[key]/antalAr, 2)

            return(totalRegionDict)

        else:
            print("Request Failed: ", response.status_code)
            # TODO: Raise exception or something.

    # Returns average numbers of suicides per year per region
    # as a JSON of key-value pairs.
    def getSuicideJson(self):
        return json.dumps(self.getSuicideDict())
