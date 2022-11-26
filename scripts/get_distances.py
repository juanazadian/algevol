import requests
from utils import *

url = "https://api.distancematrix.ai/maps/api/distancematrix/json?key=FIAYfWw4aVdT1hR7nY6YWef4EWPSf"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
