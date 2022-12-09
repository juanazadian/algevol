import requests
from utils import *

base_url = "https://api.distancematrix.ai/maps/api/distancematrix/json?key=FIAYfWw4aVdT1hR7nY6YWef4EWPSf&mode=walking"

def get_distances():
    res = []
    for index, node in enumerate(NEIGHBORHOODS_GRAPH):
        print(index)
        origin_coord = NEIGHBORHOODS_INFORMATION[index][3]
        neighbors=[]
        for neighbor in node:
            neighbor_coord = NEIGHBORHOODS_INFORMATION[neighbor[0] - 1][3]
            url = f'{base_url}&origins={origin_coord}&destinations={neighbor_coord}'
            response = requests.request("GET", url)
            json_response = response.json()
            neighbors.append( (neighbor[0], json_response["rows"][0]["elements"][0]["distance"]["value"]) )
        res.append(neighbors)
        print(res)
    print(res)

if __name__ == "__main__":
    get_distances()
