import pyrebase

def firebaseInit():
    config = {
      "apiKey": "AIzaSyDb6ZhbaZhtqLSkGy7Sme3te2ODY6mI22w",
      "authDomain": "sit-bemui.firebaseapp.com",
      "projectId": "sit-bemui",
      "storageBucket": "sit-bemui.appspot.com",
      "messagingSenderId": "208119490493",
      "appId": "1:208119490493:web:7bb16b9845b1f4e4b794d4",
      "measurementId": "G-0F7H27G5NX",
      "databaseURL": ""
    }

    return pyrebase.initialize_app(config)