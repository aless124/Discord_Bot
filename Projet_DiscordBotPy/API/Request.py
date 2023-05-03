import requests
import json
url = "https://eu-west-2.aws.data.mongodb-api.com/app/data-xuytm/endpoint/data/v1/action/findOne"
Mangas = "07 Ghost"
payload = json.dumps({
    "collection": "final_exam",
    "database": "final_exam",
    "dataSource": "Cluster0",
    
    "filter": {
        "Titre": Mangas
    }

})
headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': 'c7sn2wbTtjk7pfu5piePuokR9GBXxuENH2hO7uPhmCtFNRhursCBj4cx06VZ98rw', 
  'Accept': 'application/ejson'
}

response = requests.request("POST", url, headers=headers, data=payload)
document = response.json()["document"]
titre = document["Titre"]
origine = document["Origine"]
genres = document["Genres"]

print(response.text)

print("\n"+titre+"\n"+origine+"\n"+genres)

