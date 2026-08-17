from typing import Union
from fastapi import FastAPI

from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import GrantType, KindeApiClient

configuration = Configuration(host="https://nsfdc.kinde.com")
kinde_api_client_params = {
    "configuration": configuration,
    "domain": "https://nsfdc.kinde.com",
    "client_id": "4ef31c7cda594addbf9bee7ecc4f86fa",
    "client_secret": "5pvlwA4znZZ39nu6jnR5jueQOuwNDK0dCQjDDx2s9Qx7cvH9aUcia",
    # "grant_type": "client_credentials",
    "grant_type" : GrantType.CLIENT_CREDENTIALS,
    "callback_url": "http://localhost:8000/auth"
}
kinde_client = KindeApiClient(**kinde_api_client_params)
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/auth")
def check_auth(code: str):
    kinde_client.fetch_token(code)
    print(configuration.access_token) # Token here

    if kinde_client.is_authenticated():
        return {"Hello": code, "token" : configuration.access_token }
    else:
        return {
            "error" : "user not authenticated."
        }

@app.get("/user")
def check_user(code: str):
    kinde_client.fetch_token(code)
    return {
        "user" : kinde_client.get_user_details()
    } 

@app.get("/login")
def login():
    return { "msg" : kinde_client.get_login_url() }

@app.get("/register")
def register():
    return { "msg" : kinde_client.get_register_url() }
