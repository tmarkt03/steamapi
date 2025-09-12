import requests
import json
import mysql.connector

#http://api.steampowered.com/<interface name>/<method name>/v<version>/?key=<api key>&format=<format>

#Making a connection to the database
db = mysql.connector.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root',
    database = 'steam'
)
dbcursor = db.cursor()

#API key
key = open('key.txt')
key = key.read()

#SteamID to be used
steamid = 76561198315232228
idlist = []
idlist.append(steamid)
       

friendlist = requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={key}&steamid={steamid}&relationship=friend')
if friendlist.status_code != 200:
    print(f'Error: {friendlist.status_code}. Failed to get info from {friendlist.url}')
else:
    friendData = friendlist.json()
    friendData = friendData['friendslist']['friends']
    for i in range(len(friendData)):
        if int(friendData[i]['steamid']) not in idlist:
            idlist.append(int(friendData[i]["steamid"]))
        
    with open('friendlist.json', 'w', encoding='utf-8') as f:
        json.dump(friendlist.json(), f, ensure_ascii=False, indent=4)

i = 0
j= 0

for i in range(len(idlist)):
    dbinput = [None] * 11
    #for j in range(11):
    #        dbinput[j] = None
    playerSummary = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={idlist[i]}')
    #Checking in case the request failed
    if playerSummary.status_code != 200:
        print(f'Error: {playerSummary.status_code} Failed to get info from {playerSummary.url}')
    else:
        playerData = playerSummary.json()
        #This is the userdata that will be used in the SQL query
        dbinput =  (int(playerData["response"]["players"][0]["steamid"]), playerData["response"]["players"][0]["personaname"], playerData["response"]["players"][0]["profileurl"], playerData["response"]["players"][0]["avatar"], playerData["response"]["players"][0]["avatarmedium"], playerData["response"]["players"][0]["avatarfull"], playerData["response"]["players"][0]["personastate"], bool(playerData["response"]["players"][0]["communityvisibilitystate"]), bool(playerData["response"]["players"][0]["profilestate"]), int(playerData["response"]["players"][0]["lastlogoff"]))
        
        try:
            if bool(playerData["response"]["players"][0]["commentpermission"]):
                commentpermission = 1
            #dbinput =  (int(playerData["response"]["players"][0]["steamid"]), playerData["response"]["players"][0]["personaname"], playerData["response"]["players"][0]["profileurl"], playerData["response"]["players"][0]["avatar"], playerData["response"]["players"][0]["avatarmedium"], playerData["response"]["players"][0]["avatarfull"], playerData["response"]["players"][0]["personastate"], bool(playerData["response"]["players"][0]["communityvisibilitystate"]), bool(playerData["response"]["players"][0]["profilestate"]), int(playerData["response"]["players"][0]["lastlogoff"]), playerData["response"]["players"][0]["commentpermission"])
        except:
            commentpermission = 0
        templist = list(dbinput)
        templist.append(commentpermission)
        dbinput = tuple(templist)
        
        
        
        #Checks if the steamID is in the database
        #       >if yes then update record
        #       >if no then create new record
        dbcursor.execute(f'SELECT * FROM publicusers WHERE steamid = {dbinput[0]}')
        if len(dbcursor.fetchall()) > 0:
            print(f'SteamID already in database ({dbinput[0]}). Updating record.')
            #SQL query that updates the record
            update = "UPDATE publicusers SET personaname=%s, profileurl=%s, avatar=%s, avatarmedium=%s, avatarfull=%s, personastate=%s, communityvisibilitystate=%s, profilestate=%s, lastlogoff=%s, commentpermission=%s WHERE steamid=%s"
            tempupd = (str(dbinput[1]), dbinput[2], dbinput[3], dbinput[4], dbinput[5], dbinput[6], dbinput[7], dbinput[8], dbinput[9], dbinput[10], dbinput[0])
            dbcursor.execute(update, tempupd)
            #dbcursor.execute("UPDATE publicusers SET personaname=%s, profileurl='%s', avatar='%s', avatarmedium='%s', avatarfull='%s', personastate=%s, communityvisibilitystate=%s, profilestate=%s, lastlogoff=%s, commentpermission=%s WHERE steamid=%s" % (dbinput[2], dbinput[3], dbinput[4], dbinput[5], dbinput[6], dbinput[7], dbinput[8], dbinput[9], dbinput[10], dbinput[0]))
        else:
            print(f'New SteamID detected ({dbinput[0]}). Creating record.')
            #SQL query that creates the new record
            dbcursor.execute(f'INSERT INTO publicusers (steamid, personaname, profileurl, avatar, avatarmedium, avatarfull, personastate, communityvisibilitystate, profilestate, lastlogoff, commentpermission) VALUES {dbinput}')
        db.commit()

        #Export the request as playerSummary.json
        #DEBUG ONLY
        #with open('playerSummary.json', 'w', encoding='utf-8') as f:
        #    json.dump(playerSummary.json(), f, ensure_ascii=False, indent=4)