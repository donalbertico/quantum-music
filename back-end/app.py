import numpy as np
import csv
import os
from flask import Flask,jsonify,request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content_Type'

totalClasses = {}
for folder in os.walk('./static/assetNames'):
    for file in folder[2]:
        with open('./static/assetNames/'+file, newline='') as csvfile:
            totalClasses[file] = np.array(list(csv.reader(csvfile)))[0]
i=0
classNames = ["" for className in totalClasses]
for var in totalClasses:
    classNames[i] = var
    i += 1

def getSamples(type, num):
    count = 0
    index = np.zeros(num)
    samples = ["" for i in index]
    for i in index:
        repeat = True
        while repeat:
            possible = np.random.choice(totalClasses[type])
            if np.isin(possible,samples) :
                repeat = True
            else :
                repeat = False
                samples[count] = possible
        count += 1
    return samples

@app.route('/next')
def get_next():
    prob1 = request.args.get('prob')
    length = request.args.get('length')
    assets = request.args.get('assets')
    soundSamples = 36
    if prob1 is None : return "probability required",400
    if length is None : length = 1
    if assets is None : assets = []
    else : assets = assets.split(',')

    prob1 = int(prob1)
    prob2 = 100-int(prob1)
    totalSamples = (length*60)+5
    sounds = int((prob1*totalSamples)/100)
    silences = int((prob2*totalSamples)/100)
    soundChances = np.zeros(sounds)
    silenceChances = np.ones(silences)

    chances = np.concatenate([soundChances,silenceChances])
    np.random.shuffle(chances)
    output = ["" for chance in chances]
    binary = ["" for chance in chances]

    possibleClasses = []
    if len(assets) > 0 :
        samplesPerClass = int(soundSamples/len(assets))
        for asset in assets:
            print('asssettt',asset)
            if asset == 'cl' :
                possibleClasses = np.concatenate([possibleClasses,getSamples('clarinet.csv',samplesPerClass)])
            elif asset == 'st' :
                possibleClasses = np.concatenate([possibleClasses,getSamples('strings.csv',samplesPerClass)])
    else :
        possibleClasses = getSamples('clarinet.csv',soundSamples)

    i=0
    for chance in chances:
        binary[i] = chance
        if chance :
            output[i] = np.random.choice(totalClasses['silences.csv'])
        else :
            output[i] = np.random.choice(possibleClasses)
        i += 1

    print(output)

    return jsonify({"ids": output,"binary":binary})
