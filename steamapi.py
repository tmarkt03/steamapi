import requests
import json

#http://api.steampowered.com/<interface name>/<method name>/v<version>/?key=<api key>&format=<format>

#API key
key = "0D42AB8DF7C4200A9F811E08E4D5FF41"


response = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + key + "&steamids=76561198315232228")  
url = response.url

if response.status_code == 200:
    data = response.json()
    #print(data)
else:
    #error handling
    data = None
    print(f'Error: {response.status_code}')
    
    
#File operations
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)