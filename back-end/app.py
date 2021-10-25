import numpy as np
import csv
import os
from flask import Flask,jsonify,request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content_Type'

classes = {}
for folder in os.walk('./static/assetNames'):
    for file in folder[2]:
        with open('./static/assetNames/'+file, newline='') as csvfile:
            classes[file] = np.array(list(csv.reader(csvfile)))[0]
i=0
classNames = ["" for className in classes]
for var in classes:
    classNames[i] = var
    i += 1

@app.route('/next')
def get_next():
    prob1 = request.args.get('prob')
    length = request.args.get('length')
    if(prob1 is None): return "probability required",400
    if(length is None): length = 1

    prob1 = int(prob1)
    print('a ver',prob1,length)
    prob2 = 100-int(prob1)
    totalSamples = (length*60)+3
    clSamples = int((prob1*totalSamples)/100)
    stSamples = int((prob2*totalSamples)/100)
    clChances = np.zeros(clSamples)
    stChances = np.ones(stSamples)

    chances = np.concatenate([clChances,stChances])
    np.random.shuffle(chances)
    output = ["" for chance in chances]
    binary = ["" for chance in chances]

    i=0
    for chance in chances:
        repeat = True
        binary[i] = chance
        while repeat:
            possible = np.random.choice(classes[classNames[int(chance)]])
            if np.isin(possible,chances):
                repeat = True
            else :
                output[i] = possible
                repeat = False
        i += 1
    return jsonify({"ids": output,"binary":binary})
