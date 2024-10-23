
import requests
import requests
import json
from .banco import *

api_key = "123"
token = "otavio"
host =  "https://whatssync-api-5446ae5a5266.herokuapp.com"
#host =  "https://3f5b-191-242-51-229.ngrok-free.app"
token1 = "RANDOM_STRING_HERE"
number = "5514997763105"
token1 = "RANDOM_STRING_HERE"


def get_user_image(number):
    endpoint = f"{host}/get_user_image/{number}"
    response = requests.get(endpoint)
    return response.json()

# Function to initialize the instance v2
def init_instance_v2():
    endpoint = f"{host}/login/{api_key}"
    response = requests.post(endpoint)
    # qrcode = response.get('qrCode')
    qrcode = response.json()
    print(qrcode.get('qrCode'))
    return qrcode.get('qrCode')

# Function to get instance info v2
def instance_info_v2():
    url = f"{host}/status/123"
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    jsonresponse = response.json()

    if jsonresponse.get('message') == 'CONNECTED':
        return False
    
    return True

# Function to get base64 data
def get_base64():
    endpoint = f"{host}/get_base64"
    response = requests.get(endpoint)
    return response.json()

# Function to send text
def send_text(message):
    #endpoint = f"{host}/send_text"
    url = "http://192.168.3.11:3335/message/text?key=123"
    payload = f'id=5514997763105&message={message}'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)


def send_text(numero,message):

    url = f"{host}/send"
    print(numero)
    payload = json.dumps({
    "phone": f'"{numero}"',
    "message": f'"{message}"'
    })
    print(payload)
    headers = {'Content-Type': 'application/json','Cookie': 'csrftoken=MvSNM1T2saEjUZhtoJER67gOofjaSwAOXr67GTniBlemsVxXoNDYwAjTuzm4RZk8'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)
    insert('enviada',payload)
