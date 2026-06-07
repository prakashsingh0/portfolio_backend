from flask import Flask, request
from bson import ObjectId
from pymongo import MongoClient
from message.mail import send_mail,generate_otp, send_otp
from dotenv import load_dotenv
import os
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
client = MongoClient(os.getenv('DB_URL'))
db = client["portfolio"]
collection = db["users"]



@app.route("/",methods=["GET"])
def home():
    return ({"message":"hello kshatreeya"})

@app.route("/api/v1/users/verify/<id>", methods=["PUT"])
def verify_otp(id):

    data = request.json
    otp = str(data.get("otp"))

    user = collection.find_one({
        "_id": ObjectId(id)
    })

    if user is None:
        return {
            "success": False,
            "message": "User not found"
        }, 404

    if user.get("verified", False):
        return {
            "success": True,
            "message": "Already verified"
        }, 200

    user_otp = str(user.get("otp"))

    if otp != user_otp:
        return {
            "success": False,
            "message": "Invalid OTP"
        }, 400

    collection.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {"verified": True},
            "$unset": {"otp": ""}
        }
    )

    mresponse = send_mail(
        email=user.get("email"),
        name=user.get("name"),
        subject=user.get("subject"),
        message=user.get("message"),
        phone=user.get("phone")
    )

    if mresponse.get("status") == "successful":
        return {
            "success": True,
            "message": "Verified successfully"
        }, 200

    return {
        "success": False,
        "message": "Email sending failed"
    }, 500


@app.route("/api/v1/users/contact",methods=["POST"])
def constact():
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        message = data.get("message")
        subject = data.get("subject")
        print(data)

        if not data.get("email"):
            return ({"success":False, "message":"Email is required"}, 400)
        user = collection.find_one({"email":data["email"]})
        if user:
            if user.get("verified",True):

                if collection.find_one({"email":data["email"]}):
                
                    mail_response = send_mail(email=email, name=name, subject=subject,message=message,phone=phone)
                    print(mail_response)
                    if mail_response.get("status") == "successful":

                        return ({"success":True,"verified":True,"message":"Email is already register we will contact you soon"},200)
        
        else:
            otp = generate_otp()
            email_otp = send_otp(email=email, otp=otp, name=name)
            if email_otp:

                data['otp'] = otp
                result = collection.insert_one(data)

                return ({"success":True,"message": "Your query received we will contact soon", "_id":str(result.inserted_id)}, 201)

    except Exception as e:
        return {
        "success": False,
        "error": str(e)
    }, 500



if __name__ == "__main__":
    app.run()

