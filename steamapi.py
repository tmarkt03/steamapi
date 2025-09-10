import requests
import json
import mysql.connector

#http://api.steampowered.com/<interface name>/<method name>/v<version>/?key=<api key>&format=<format>

#List of API methods
apilist = requests.get(f'https://api.steampowered.com/ISteamWebAPIUtil/GetSupportedAPIList/v0001/')

db = mysql.connector.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root',
    database = 'steam'
)
dbcursor = db.cursor()

#Checks if the request is valid and writes to apilist.json
if apilist.status_code != 200:
    print(f'Error: {apilist.status_code}. Failed to get info from {apilist.url}')
else:
    with open('list.json', 'w', encoding='utf-8') as f:
        json.dump(apilist.json(), f, ensure_ascii=False, indent=4)

#API key
key = open('key.txt')
key = key.read()

playerSummary = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids=76561198315232228')

if playerSummary.status_code != 200:
    print(f'Error: {playerSummary.status_code} Failed to get info from {playerSummary.url}')
else:
    with open('playerSummary.json', 'w', encoding='utf-8') as f:
        json.dump(playerSummary.json(), f, ensure_ascii=False, indent=4)


clientver = requests.get('http://api.steampowered.com/IGCVersion_1046930/GetClientVersion/v0001/')

if clientver.status_code != 200:
    print(f'Error: {clientver.status_code}. Failed to get info from {clientver.url}')
else:
    with open('clientver.json', 'w', encoding='utf-8') as f:
        json.dump(clientver.json(), f, ensure_ascii=False, indent=4)