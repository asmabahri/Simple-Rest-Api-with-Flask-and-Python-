"""
Registration of a user 0 tokens
each user gets 10 tokens
store a sentence on our database for 1 token
retrive his store sentence on our database for 1 token

"""

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)
client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["users"]

class register(Resource):
   def Post(self):
    #step1 is to get posted data by the user
    postedData = request.get_json()
    
    #get the data
    username = postedData["username"]
    password = postedData["password"]

    #hash[password+salt]=hashing the passwords using py-Bcrypt
    hashed_pw= bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

    #store pass and username to the db
    users.insert({
        "username":username,
        "password":hashed_pw,
        "sentence":"",
        "Tokens": 6
        })

    retJson= {
       "Status":200,
       "msg": "you successfully signed up for Api"
    }
    return jsonify(retJson)


def verify_pw(username,password):
    hashed_pw = users.find({
        "username":username,

        })[0]["password"]
    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
         return False   
def  countTokens(username):
    tokens = users.find({
        "username":username
        #access the usre's tokens
    })[0]["Tokens"] 
    return tokens         
class store(Resource):
    def Post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]
        #verify username pw match

        correct_pw = verify(username, password)
        if not correct_pw:
            retJson= {
                "Status":302
            }
            return jsonify(retJson)

        #verify user have enough 
        num_tokens = countTokens(username)
        if not num_tokens <= 0:
            retJson = { 
                "Status": 301
            }
            return jsonify(retJson)
        users.update({{
            "username": username
            },
            {"$set":{"sentence":sentence},
            "Tokens":num_tokens-1}
        })   
        retJson = {
           "Status":200,
           "msg": "sentence saved successfully"

        } 
        return jsonify(retJson)



api.add_resource(register,"/register")
api.add_resource(store,"/store")
if __name__=="__main__":
    app.run(host='0.0.0.0')

"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import os

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert({
    'num_of_users':0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num + 1
        UserNum.update({}, {"$set":{"num_of_users":new_num}})
        return str("Hello user " + str(new_num))


def checkPostedData(postedData, functionName):
    if (functionName == "add" or functionName == "subtract" or functionName == "multiply"):
        if "x" not in postedData or "y" not in postedData:
            return 301 #Missing parameter
        else:
            return 200
    elif (functionName == "division"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif int(postedData["y"])==0:
            return 302
        else:
            return 200

class Add(Resource):
    def post(self):
        #If I am here, then the resouce Add was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "add")
        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Add the posted data
        ret = x+y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

class Subtract(Resource):
    def post(self):
        #If I am here, then the resouce Subtract was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "subtract")


        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Subtract the posted data
        ret = x-y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)


class Multiply(Resource):
    def post(self):
        #If I am here, then the resouce Multiply was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "multiply")


        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Multiply the posted data
        ret = x*y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

class Divide(Resource):
    def post(self):
        #If I am here, then the resouce Divide was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "division")


        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Multiply the posted data
        ret = (x*1.0)/y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)



api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/division")
api.add_resource(Visit, "/hello")

@app.route('/')
def hello_world():
    return "Hello World!"


if __name__=="__main__":
    app.run(host='0.0.0.0')
"""