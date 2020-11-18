from flask import Flask, request, jsonify
# from models import todo  # call model file
from flask_cors import CORS  # to avoid cors error in different frontend like react js or any other
from pymongo import MongoClient
import pymongo
from bson import ObjectId,json_util
import os
import json


global absDirName
absDirName = os.path.dirname(os.path.abspath(__file__))

def mongoconnection():
    with open(os.path.join(absDirName,"constants.json"),"r")  as constants:
        global constantsData
        constantsData = json.load(constants)

    global uri 
    # uri = "mongodb://" +constantsData['username'] + ":" + constantsData['password'] + "@" + constantsData["server"] +":" + constantsData['port'] + "/dgsafe?ssl=false&authSource=dgsafe"
    # 'mongodb://dgadminreadWrite:Dg-Tt-Wh-2020@11.0.24.31:52498/dgsafe?ssl=false&authSource=dgsafe'
    uri = "mongodb+srv://IamWaddy:"+ constantsData['password'] + "@cluster-alpha.1vji7.mongodb.net/demoDatabase?retryWrites=true&w=majority"
    print (uri)
    client = pymongo.MongoClient(uri)
    # client = MongoClient(uri)
    global demoDatabase
    demoDatabase = client.demoDatabase
    global loginModel
    loginModel = demoDatabase["loginModel"]
    # portfolio = client["portfolio"]


mongoconnection()

app = Flask(__name__)
CORS(app)

# todo = todo.Todo()

def data_sanitizer(data):
    data_sanitized = json.loads(json_util.dumps(data))
    return data_sanitized

@app.route('/login/', methods=['POST'])
def login():
    requesData = json.loads(request.data)
    # print("Ïam Here .... ", requesData, type(requesData))
    if ("email" in requesData and "password" in requesData):
        # data = data_sanitizer(list(loginModel.find({"email":requesData["email"].lower()}))
        data = data_sanitizer(list(loginModel.find({"email":requesData["email"].lower()})))
        print(data)
        if (len(data) == 0):
            obj = {"status":404, "message": "User Doesn't Exists" }
            response = app.response_class(response={ json.dumps(obj) }, status=404, mimetype='application/json')
        else:
            data = data[0]
            if requesData["password"] == data["password"]:
                obj = {"status":200, "results":data}
                response = app.response_class(response={ json.dumps(obj)}, status=200, mimetype='application/json')
            else:
                obj = {"status":403, "message":'password Incorrect'}
                response = app.response_class(response={ json.dumps(obj) }, status=403, mimetype='application/json')
    # print(data)
    return response



if __name__ == '__main__':
    app.run(debug=True)
