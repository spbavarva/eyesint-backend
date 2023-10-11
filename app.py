import pymongo
from flask import Flask, request, jsonify
from flask_cors import CORS  
from pymongo import MongoClient
from bson.json_util import dumps
from header import headers
from whoiss import whois_lookup
from sslnew import ssl_analyzer
from mailex import mail
from crawler import crawlmain
import asyncio
from phone import number
from name import nameinfo
from pdf import pdfinfo
from domain import domainS

loop = asyncio.get_event_loop()

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("mongodb+srv://shenvakalpesh4:z0LDlMgGlqs1BWBZ@cluster0.yg1kuiy.mongodb.net/?retryWrites=true&w=majority")
db = client["Eyesint"]  
users_collection = db["users"]

# Register route
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Check if the email is already registered
    if users_collection.find_one({"email": email}):
        return jsonify({"message": "Email is already registered"}), 400

    # Insert the user into the database
    user = {
        "username": username,
        "email": email,
        "password": password,  # Note: You should hash the password before storing it
    }
    users_collection.insert_one(user)

    return jsonify({"message": "Registration successful"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Check if a user with the provided email and password exists in the database
    user = users_collection.find_one({"email": email, "password": password})

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401


@app.route("/web/header",methods=["POST"])
def get_header():
    data=request.get_json()
    url=data.get("url")
    result=headers(url)
    print(result)
    return jsonify({"data":result}), 200

@app.route("/web/whoiss",methods=["POST"])
def get_whois():
    data=request.get_json()
    url=data.get("url")
    result=whois_lookup(url)
    print(result)
    return jsonify({"data":result}), 200

@app.route("/web/ssl", methods=["POST"])
def get_ssl():
    data = request.get_json()
    url = data.get("url")
    result = ssl_analyzer(url)
    print(result)

    # Return the result as JSON response
    return jsonify({"data": result}), 200 

@app.route("/web/mailex", methods=["POST"])
def get_mail():
    data = request.get_json()
    url = data.get("url")
    result = mail(url)
    print(result)
    return jsonify({"data": result}), 200 

@app.route("/web/crawlmain", methods=["POST"])
def get_crawl():
    data = request.get_json()
    url = data.get("url")
    output = []
    # data={}
    crawl_results = crawlmain(url, output, data)
    return jsonify({"data": crawl_results}), 200

@app.route("/foot/phone", methods=["POST"])
def get_number():
    data = request.get_json()
    url = data.get("url")
    result = number(url)
    print(result)
    return jsonify({"data": result}), 200 

@app.route("/foot/nameinfo", methods=["POST"])
def get_name():
    data = request.get_json()
    url = data.get("url")
    result = nameinfo(url)
    print(result)
    return jsonify({"data": result}), 200 

@app.route("/foot/domainS", methods=["POST"])
def get_domain():
    data = request.get_json()
    domain = data.get("url")  # Change "url" to "domain" to match the frontend input
    # Call the domainS function to fetch domain information
    result = domainS(domain)
    print(result)
    # Return the result as a JSON response to the frontend
    return jsonify({"data": result}), 200


@app.route("/foot/pdfinfo", methods=["POST"])
def get_pdf():
    try:
        file = request.files["file"]
        if file:
            # Save the uploaded file temporarily (optional)
            file_path = "temp.pdf"  # Change the path as needed
            file.save(file_path)

            # Call pdfinfo function to extract metadata
            metadata = pdfinfo(file_path)

            # Remove the temporary file if needed
            # os.remove(file_path)

            return jsonify({"data": metadata}), 200
        else:
            return jsonify({"message": "Please select a PDF file."}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Example route to fetch all users from the database
@app.route("/users", methods=["GET"])
def get_users():
    users = list(users_collection.find({}))
    return dumps(users)

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)