
# WHERE WILL MY SENATORS BE
## BASED ON UPCOMING 20 SENATE COMMITTEE HEARINGS (COMPLETED)
### REQUIRES USERS INPUT FOR CHOOSING A STATE (COMPLETED)
## BASED ON FLOOR VOTES DATA (NOT STARTED)


import pandas as pd
import requests
import datetime
import sys
import json
#auth = 'qX4ESvMAECYCHKTLSdMlVJZwF9X6nd0NfDiLZyLt'
headers = {'X-API-Key':'qX4ESvMAECYCHKTLSdMlVJZwF9X6nd0NfDiLZyLt'}




## GETTING SENATORS INFO (ID, NAME) BASED ON STATE (CURRENT IN-OFFICE)




state = input('Enter state abbreviations: ').upper()

url = 'https://api.propublica.org/congress/v1/115/senate/members.json'

response = requests.get(url, headers=headers)

#Catching request error
if response.status_code != 200:
    if response.status_code == 400:
        print('Bad Request – Your request is improperly formed')
    elif response.status_code == 403:
        print('Forbidden – Your request did not include an authorization header')
    elif response.status_code == 404:
        print('Not Found – The specified record(s) could not be found')
    elif response.status_code == 406:
        print('Not Acceptable – You requested a format that isn’t json or xml')
    elif response.status_code == 500:
        print('Internal Server Error – We had a problem with our server. Try again later.')
    elif response.status_code == 503:
        print('Service Unavailable – The service is currently not working. Please try again later.')
    else:
        print('Some error occured')

#Settting up Lists for Senator Info   
senator_ID = []
senator_fName = []
senator_lName = []

data = response.json()

#Finds Senators Info by looping through each member and checking their state
if (data['status'] == 'OK'):
    results = data['results'][0]['members']
    for x in results:
        if x['state'] == state:
            if x['in_office'] == True:
                print ('Senator', x['first_name'], x['last_name'])
                print ('ID: ', x['id'])
                            
                senator_ID.append(x['id'])
                senator_fName.append(x['first_name'])
                senator_lName.append(x['last_name'])
                
    #Exits program if the given state does not exist
    if len(senator_ID) == 0:
        print('** State could not be found, please check spelling of the state abbreviation **')
        sys.exit('State could not be found, please check spelling of the state abbreviation')
        
else:
    print('Sorry! There is some problem retrieving data. Data Status != OK')




## GETTING THE LIST OF ALL COMMITTEES ID




url2 = 'https://api.propublica.org/congress/v1/115/senate/committees.json'

response = requests.get(url2, headers = headers)

#Catching request error
if response.status_code != 200:
    if response.status_code == 400:
        print('Bad Request – Your request is improperly formed')
    elif response.status_code == 403:
        print('Forbidden – Your request did not include an authorization header')
    elif response.status_code == 404:
        print('Not Found – The specified record(s) could not be found')
    elif response.status_code == 406:
        print('Not Acceptable – You requested a format that isn’t json or xml')
    elif response.status_code == 500:
        print('Internal Server Error – We had a problem with our server. Try again later.')
    elif response.status_code == 503:
        print('Service Unavailable – The service is currently not working. Please try again later.')
    else:
        print('Some error occured')

committees_id = []

#Returns all the Senate Committee Id into the array committees_id
data = response.json()
if (data['status'] == 'OK'):
    results = data['results'][0]['committees']
    for x in results:
        committees_id.append(x['id'])
else:
    print('Sorry! There is some problem retrieving data. Data Status != OK')
    
    
    
        
## SETTING UP URLS FOR EACH COMMITTEE ID INTO A LIST
    ## Each committee data is in its own URL
       
    
    
    
committee_URLS = []

for x in committees_id:
    committee_URLS.append('https://api.propublica.org/congress/v1/115/senate/committees/'
                          + x + '.json')




## FINDING THE COMMITTEE MEMBERSHIP FOR SENATORS INTO THEIR OWN LIST
    
    
    
    
#Lists to store committee id for each senator
senator_1_committee = []
senator_2_committee = []

#Goes through each of the stored URL
for x in committee_URLS:
    response_URL = requests.get(x, headers = headers)
    
    #Catching request error
    if response.status_code != 200:
        if response.status_code == 400:
            print('Bad Request – Your request is improperly formed')
        elif response.status_code == 403:
            print('Forbidden – Your request did not include an authorization header')
        elif response.status_code == 404:
            print('Not Found – The specified record(s) could not be found')
        elif response.status_code == 406:
            print('Not Acceptable – You requested a format that isn’t json or xml')
        elif response.status_code == 500:
            print('Internal Server Error – We had a problem with our server. Try again later.')
        elif response.status_code == 503:
            print('Service Unavailable – The service is currently not working. Please try again later.')
        else:
            print('Some error occured')
            
    #Checks each committee to see if the senators from given state are members
    #of the committee
    data_URL = response_URL.json()
    if (data_URL['status'] == 'OK'):
        name_URL = data_URL['results'][0]['name']
        code_URL = data_URL['results'][0]['id']
        results_URL = data_URL['results'][0]['current_members']
        for x in results_URL:
            if x['id'] in senator_ID[0]:
                senator_1_committee.append(code_URL)
            if x['id'] in senator_ID[1]:
                senator_2_committee.append(code_URL)
  
    else:
        print('Sorry! There is some problem retrieving data. Data Status != OK')
    
    
    
    
## TURNING SENATORS INFO (ID, NAME) INTO A DATAFRAME




senatordf = pd.DataFrame(
        {'ID': senator_ID,
         'First Name': senator_fName,
         'Last Name': senator_lName})


          
    
## GETTING UPCOMING COMMITTEE HEARING DATE/TIME FOR THE TWO SENATORS



    
url3 = 'https://api.propublica.org/congress/v1/115/senate/committees/hearings.json'

response = requests.get(url3, headers = headers)

#Catching request error
if response.status_code != 200:
    if response.status_code == 400:
        print('Bad Request – Your request is improperly formed')
    elif response.status_code == 403:
        print('Forbidden – Your request did not include an authorization header')
    elif response.status_code == 404:
        print('Not Found – The specified record(s) could not be found')
    elif response.status_code == 406:
        print('Not Acceptable – You requested a format that isn’t json or xml')
    elif response.status_code == 500:
        print('Internal Server Error – We had a problem with our server. Try again later.')
    elif response.status_code == 503:
        print('Service Unavailable – The service is currently not working. Please try again later.')
    else:
        print('Some error occured')
    
data = response.json()

if data['status'] == 'OK':
    results = data['results'][0]['hearings']
    
    #Goes through each hearing to display results of senators location
    for x in results:
        
        #compares date-time of each hearing to only display upcoming hearing      
        dateTime = x['date'] + ' ' + x['time']
        dateTime = datetime.datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
        
        CurrentDate = datetime.datetime.now()
        
        if (dateTime > CurrentDate):
        
            if (x['committee_code'] in senator_1_committee):
                print('\n' + 'Senator', 
                      senatordf['First Name'][0], senatordf['Last Name'][0],
                      'from', state, 'will be in', x['location'],
                      'on ', x['date'], 'at ', x['time'], 'for',
                      x['description']) 
                    
            if (x['committee_code'] in senator_2_committee):
                print('\n' + 'Senator', 
                      senatordf['First Name'][1], senatordf['Last Name'][1],
                      'from', state, 'will be in', x['location'],
                      'on ', x['date'], 'at ', x['time'], 'for',
                      x['description']) 

    print ('\n' + 'Program Finished Executing, no result = no recent upcoming schedule available')
else:
    print('Sorry! There is some problem retrieving data. Data Status != OK')