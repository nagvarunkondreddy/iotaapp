from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import pyrebase
import requests

class register(BaseModel):
    email:str
    password:str

class login(BaseModel):
    email:str
    password:str
class reset(BaseModel):
    email:str

app = FastAPI()
firebaseConfig = {
    "apiKey": "AIzaSyBgJ_HwnPvzWGYlfDYyA0oTDBn0YmK6ACA",
    "authDomain": "iotaapp-5076c.firebaseapp.com",
    "databaseURL": "https://iotaapp-5076c.firebaseio.com",
    "projectId": "iotaapp-5076c",
    "storageBucket": "iotaapp-5076c.appspot.com",
    "messagingSenderId": "840390642652",
    "appId": "1:840390642652:web:df87d5af43a9cb1bf39d19",
    "measurementId": "G-LS7QT4FB1Z"
}
firebase=pyrebase.initialize_app(firebaseConfig)
auth= firebase.auth()

@app.post("/register")
def register(item: register):
    user=auth.create_user_with_email_and_password(item.email,item.password)
    auth.send_email_verification(user['idToken'])
    if (user):
        return "registered"
    else:
        return "not registered"

@app.post("/login")
def login(item:login):
    try:
        user=auth.sign_in_with_email_and_password(item.email,item.password)
        res=auth.get_account_info(user['idToken'])
        if(str(res['users'][0]['emailVerified']) == "False"):
            return("email not verified")
        else:
            return("logged in")
    except Exception as e:
        print(e)
        return(e)


@app.post("/resetPassword")
def resetPassword(item:reset):
    try:
        user=auth.send_password_reset_email(item.email)
        return("reset mail sent")
    except Exception as e:
        print(e)
        return(e)




