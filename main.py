#!/usr/bin/python

# Usage of lib request
# http://docs.python-requests.org/en/master/
import requests

serverDomain = 'http://192.168.1.10:3000'

def handleResponse(response):
    if response.status_code == 200:
        body_json = response.json()

        if 'error' in body_json:
            print(body_json['error'])
        else:
            if body_json['gameOver']:
                print("Game over. Here are the results :")
                body_json['results']['nbCuredPatients'] = len(body_json['results']['curedPatients'])
                print(body_json['results'])
            else:
                play(body_json['gameId'], body_json['state'])
    else:
        print("Error : server returned status code "+response.status_code)


def play(gameId, curState):
    move = turn(curState)
    if move is not None:
        payload = {'gameId': gameId, 'action': move}
        r = requests.post(serverDomain + '/api/play', data=payload)
        handleResponse(r)


def start(patientId):
    r = requests.post(serverDomain + '/api/start', data={'patientId': patientId})
    handleResponse(r)

# createResponseHandler(playCB));


def evaluate(teamName):
    r = requests.post(serverDomain + '/api/evaluate', data={'teamName': teamName})
    handleResponse(r)


# createResponseHandler(playCB));


def turn(curstate):
    print(curstate)
    if curstate['visitCount'] == 0:
        return {'type': 'WAIT'}
    elif curstate['visitCount'] == 1:
        return {'type': 'TREATMENT', 'treatment': 'Detoxifier' }
    else:
        return {'type': 'TREATMENT', 'treatment': 'Antibio1' }

# To run your code with only one patient, use this function. The integer is the id of the patient
start(1)

# To test your code and evaluate your score, use this function. Your code will run for all the patients available
#evaluate("Olist")

