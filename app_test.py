import requests
import json

url = "http://127.0.0.1:4000/prediction"

payload = json.dumps({

    "Latitude" : 21.456700,
    "Longitude" : 80.218280
})

headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)


print(response.text)