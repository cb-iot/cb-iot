#!/usr/bin/python

# Usage of lib request
# http://docs.python-requests.org/en/master/
import requests
import pprint
import json

serverDomain = 'http://192.168.1.10:3000'

turnData = {}
patientsCured = 0
treatmentList = (None, "Detoxifier", "Antibio1", "Antibio2", "Antibio3", "Antiviral1", "Antiviral2", "Antiviral3")

def handleResponse(response):
    global patientsCured
    if response.status_code == 200:

        body_json = response.json()

        if 'error' in body_json:
            print(body_json)
            print(body_json['error'])
        else:
            if body_json['gameOver']:
                print("Game over. Here are the results :")
                body_json['results']['nbCuredPatients'] = len(body_json['results']['curedPatients'])
                patientsCured += body_json['results']['nbCuredPatients']
                print body_json['results']
            else:
                play(body_json['gameId'], body_json['state'])
    else:
        print("Error : server returned status code "+response.status_code)



def play(gameId, curState):
    move = turn(curState)
    if move is not None:
        payload = {'gameId': gameId, 'action': move}
        r = requests.post(serverDomain + '/api/play', json=payload)
        handleResponse(r)

def getPatient(patientId):
    r = requests.post(serverDomain + '/api/start', json={'patientId': patientId})
    return r.json()

def start(patientId):
    r = requests.post(serverDomain + '/api/start', json={'patientId': patientId})
    handleResponse(r)

# createResponseHandler(playCB));


def evaluate(teamName):
    r = requests.post(serverDomain + '/api/evaluate', json={'teamName': teamName})
    handleResponse(r)


# createResponseHandler(playCB));

lastHealth = 100


def turn(curstate):
    global lastHealth
    curHealth = curstate['health']
    print(curHealth)

    if curHealth > lastHealth:
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    lastHealth = curHealth


    return turnData
    if curstate['visitCount'] == 0:
        print "waiting"
        return {'type': 'WAIT'}
    elif curstate['visitCount'] == 1:
        print "doing detox"
        return {'type': 'TREATMENT', 'treatment': 'Detoxifier' }
    else:
        print "doing antibio"
        return {'type': 'TREATMENT', 'treatment': 'Antibio1' }

"""
# To run your code with only one patient, use this function. The integer is the id of the patient
for t in treatmentList:
    patientsCured = 0
    if t is None:
        turnData = {'type': 'WAIT'}
    else:
        turnData = {'type': 'TREATMENT', 'treatment': t }

    print "++++++++++++++++++ Trying out treatment", t
    #print "++++++++++++++++++"
    #print "++++++++++++++++++"

    for i in range(6):
        lastHealth = 100
        #print "======================== Trying out number", i
        start(i)

    print "============================================Results (patientscured)", patientsCured, "for treatment", t

# To test your code and evaluate your score, use this function. Your code will run for all the patients available
"""

turnData = {'type': 'TREATMENT', 'treatment': "Detoxifier" }
evaluate("BelgoRussian1")


#pprint.pprint(getPatient(1))
