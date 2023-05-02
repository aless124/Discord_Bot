import requests
import json
url = "https://eu-west-2.aws.data.mongodb-api.com/app/data-xuytm/endpoint/data/v1/action/findOne"

payload = json.dumps({
    "collection": "final_exam",
    "database": "final_exam",
    "dataSource": "Cluster0",
    "projection": {
        "Date de sortie": 2005,
    }
})
headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': 'c7sn2wbTtjk7pfu5piePuokR9GBXxuENH2hO7uPhmCtFNRhursCBj4cx06VZ98rw', 
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
