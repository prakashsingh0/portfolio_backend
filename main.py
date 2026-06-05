from flask import Flask, request
from bson import ObjectId
from pymongo import MongoClient
from message.mail import send_mail
from dotenv import load_dotenv
import os

app = Flask(__name__)

client = MongoClient(os.getenv('DB_URL'))
db = client["portfolio"]
collection = db["users"]



@app.route("/",methods=["GET"])
def home():
    return ({"message":"hello kshatreeya"})


@app.route("/api/v1/contact",methods=["POST"])
def constact():
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        message = data.get("message")
        subject = data.get("subject")

        if not data.get("email"):
            return ({"success":False, "message":"Email is required"}, 400)
        if collection.find_one({"email":data["email"]}):

            mail_response = send_mail(email=email, name=name, subject=subject)
            print(mail_response)
            if mail_response.get("status") == "successful":

                return ({"success":True,"message":"Email is already register we will contact you soon"},200)
        
        else:
            result = collection.insert_one(data)
            mresponse = send_mail(email=email, name=name, subject=subject)
            print(mresponse)
            if mresponse.get("status") == "successful":

                return ({"success":True,"message": "Your query received we will contact soon", "_id":str(result.inserted_id)}, 201)
            
    except Exception as e:
        return {
        "success": False,
        "error": str(e)
    }, 500



if __name__ == "__main__":
    app.run()

