import requests
import json
import time
import sys
import multiprocessing

import psycopg

#http://api.steampowered.com/<interface name>/<method name>/v<version>/?key=<api key>&format=<format>

class Requests:
    key = open('key.txt')
    key = key.read()
    idlist = []
    idlist.append(76561198315232228)
    calls = 0
    maxcalls = 300

#SHOWCASE
def updatedb(value):
    with psycopg.connect("dbname=steam user=postgres") as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE publicusers SET personaname=%s, profileurl=%s, avatar=%s, avatarmedium=%s, avatarfull=%s, personastate=%s, communityvisibilitystate=%s, profilestate=%s, lastlogoff=%s, commentpermission=%s WHERE steamid=%s")



def GetAppList():
    with psycopg.connect("dbname=postgres user=postgres") as conn:
        with conn.cursor() as cur:
            try:
                req = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
                Requests.calls += 1
            except:
                print('Failed to get response from steam')

            json = req.json()
            appid = []
            name = []
            for i in range (len(json['applist']['apps'])):
                appid.append(json['applist']['apps'][i]['appid'])
                name.append(json['applist']['apps'][i]['name'])

            applist = {
                'appid': appid,
                'name' : name
            }
            for i in range(len(applist['appid'])):
                cur.execute("SELECT appid FROM applist WHERE appid = %s", (applist['appid'][i],))
                #print('sql error in applist')
                #cur.execute(f'INSERT INTO applist (appid, name) VALUES {applist["appid"][i], applist["name"][i]}')
                if cur.fetchone() == None:
                    temp1 = applist["appid"][i]
                    temp2 = applist["name"][i]
                    cur.execute("INSERT INTO applist (appid, name) VALUES (%s, %s);", (applist["appid"][i], applist["name"][i]))
            conn.commit()
    
    
def GetFriendList():
    while Requests.calls + (len(Requests.idlist) // 100) <= Requests.maxcalls:
        #try:
        req = requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={Requests.key}&steamid={Requests.idlist[Requests.calls]}&relationship=friend')
        Requests.calls += 1
        #except:
            #print('Request failed')
        if req.status_code == 401:
            print(f'Error {req.status_code} Friendlist probably private skipping...')
        elif req.status_code == 429:
            print('\n\nERROR 429: TOO MANY REQUESTS')
            sys.stdout.write('Trying again in 3.5 seconds')
            time.sleep(1)
            sys.stdout.write('.')
            time.sleep(1)
            sys.stdout.write('.')
            time.sleep(1)
            sys.stdout.write('.\n')
            time.sleep(0.5)
        elif req.status_code != 200:
            print(f'Error: {req.status_code}. Failed to get info from {req.url}')
        else:
            json = req.json()
            json = json['friendslist']['friends']
            for i in range(len(json)):
                if int(json[i]['steamid']) not in Requests.idlist:
                    Requests.idlist.append(int(json[i]["steamid"]))
                    print(len(Requests.idlist))
    return(Requests.idlist, len(Requests.idlist), Requests.calls)


if __name__ == '__main__':
    #Making a connection to the database
    #API key
    #key = open('key.txt')
    #key = key.read()
#
    ##SteamIDs and all lists in connection with them
    #steamid = 76561198315232228
    #
    ##The number of api calls
    #maxcalls = 10
    #calls = 0
    
    #Stats for the end of the script
    statupdate = 0
    statnew = 0
    statround = [0, 0, 0]
    
    GetFriendList()
    
    #Crawl all the public friendslists and adds them to idlist if they are not in it yet
    #while calls + (len(idlist) // 100) <= maxcalls:
    #    print(f'{calls} calls.')
    #    try:
    #        friendlist = requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={key}&steamid={idlist[calls]}&relationship=friend')
    #        calls = calls + 1
    #    except:
    #        print('Request failed waiting for 1 minute...')
    #        time.sleep(60)
    #        friendlist = requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={key}&steamid={idlist[calls]}&relationship=friend')
    #        calls = calls + 1
    #    #idlist.append(idlist.pop())
    #    
    #    
    #    #ERROR HANDLING
    #    # 401: In this case it is probably because the friend list is private
    #    # 429: Too many requests (wait for 3.5 seconds)
    #    if friendlist.status_code == 401:
    #        print(f'Error {friendlist.status_code} Friendlist probably private skipping...')
    #    elif friendlist.status_code == 429:
    #        print('\n\nERROR 429: TOO MANY REQUESTS')
    #        sys.stdout.write('Trying again in 3.5 seconds')
    #        time.sleep(1)
    #        sys.stdout.write('.')
    #        time.sleep(1)
    #        sys.stdout.write('.')
    #        time.sleep(1)
    #        sys.stdout.write('.\n')
    #        time.sleep(0.5)
    #    elif friendlist.status_code != 200:
    #        print(f'Error: {friendlist.status_code}. Failed to get info from {friendlist.url}')
    #    else:
    #        friendData = friendlist.json()
    #        friendData = friendData['friendslist']['friends']
    #        for i in range(len(friendData)):
    #            if int(friendData[i]['steamid']) not in idlist:
    #                idlist.append(int(friendData[i]["steamid"]))
    #print(GetFriendList())

    #while 0 < len(idlist) and calls < maxcalls:
    #    time.sleep(0.05)
    #    j = 0
    #    k = 0
    #    playerSummary = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={idlist[0:99]}')
    #    calls + 1
    #    
    #    #ERROR HANDLING
    #    # 429: Too many requests (wait for 3.5 seconds)
    #    if playerSummary.status_code == 429:
    #        print('\n\nERROR 429: TOO MANY REQUESTS')
    #        sys.stdout.write('Trying again in 3.5 seconds')
    #        time.sleep(1)
    #        sys.stdout.write('.')
    #        time.sleep(1)
    #        sys.stdout.write('.')
    #        time.sleep(1)
    #        sys.stdout.write('.\n')
    #        time.sleep(0.5)
    #    #Some unexpected error
    #    elif playerSummary.status_code != 200:
    #        print(f'Error: {playerSummary.status_code} Failed to get info from {playerSummary.url}')
    #    else:            
    #        playerData = playerSummary.json()
    #        statround[2] = statround[2] + 1
    #        #We format the data then enter it into the database here
    #        for j in range(len(playerData["response"]["players"])):
    #            dbinput = [None] * 11
    #            #This is the userdata that will be used in the SQL query
    #            dbinput =  (int(playerData["response"]["players"][j]["steamid"]), playerData["response"]["players"][j]["personaname"], playerData["response"]["players"][j]["profileurl"], playerData["response"]["players"][j]["avatar"], playerData["response"]["players"][j]["avatarmedium"], playerData["response"]["players"][j]["avatarfull"])
    #            #We need to use try cases because there are cases they aren't present in the json
    #            try:
    #                personastate = int(playerData["response"]["players"][j]["personastate"])
    #                temp = list(dbinput)
    #                temp.append(personastate)
    #                dbinput = tuple(temp)
    #            except:
    #                personastate = 0
    #                temp = list(dbinput)
    #                temp.append(personastate)
    #                dbinput = tuple(temp)
    #            try:
    #                comvis = bool(playerData["response"]["players"][j]["communityvisibilitystate"])
    #                temp = list(dbinput)
    #                temp.append(comvis)
    #                dbinput = tuple(temp)
    #            except:
    #                comvis = False
    #                temp = list(dbinput)
    #                temp.append(comvis)
    #                dbinput = tuple(temp)
    #            try:
    #                profilestate = bool(playerData["response"]["players"][j]["profilestate"])
    #                temp = list(dbinput)
    #                temp.append(profilestate)
    #                dbinput = tuple(temp)
    #            except:
    #                profilestate = False
    #                temp = list(dbinput)
    #                temp.append(profilestate)
    #                dbinput = tuple(temp)
    #            try:
    #                lastlogoff = int(playerData["response"]["players"][j]["lastlogoff"])
    #                temp = list(dbinput)
    #                temp.append(lastlogoff)
    #                dbinput = tuple(temp)
    #            except:
    #                lastlogoff = 0
    #                temp = list(dbinput)
    #                temp.append(lastlogoff)
    #                dbinput = tuple(temp)
    #            try:
    #                if bool(playerData["response"]["players"][j]["commentpermission"]):
    #                    commentpermission = bool(playerData["response"]["players"][j]["commentpermission"])
    #                    temp = list(dbinput)
    #                    temp.append(commentpermission)
    #                    dbinput = tuple(temp)
    #            except:
    #                commentpermission = False
    #                temp = list(dbinput)
    #                temp.append(commentpermission)
    #                dbinput = tuple(temp)
    #            #Checks if the steamID is in the database
    #            #       >if yes then update record
    #            #       >if no then create new record
    #            dbcursor.execute(f'SELECT * FROM publicusers WHERE steamid = {dbinput[0]}')
    #            if len(dbcursor.fetchall()) > 0:
    #                #SQL query that updates the record in case it already exists
    #                #We use local variables to handle special characters in usernames (because the query is sensitive to commas)
    #                update = "UPDATE publicusers SET personaname=%s, profileurl=%s, avatar=%s, avatarmedium=%s, avatarfull=%s, personastate=%s, communityvisibilitystate=%s, profilestate=%s, lastlogoff=%s, commentpermission=%s WHERE steamid=%s"
    #                tempupd = (str(dbinput[1]), dbinput[2], dbinput[3], dbinput[4], dbinput[5], dbinput[6], dbinput[7], dbinput[8], dbinput[9], dbinput[10], dbinput[0])
    #                dbcursor.execute(update, tempupd)
    #                statupdate = statupdate + 1
    #                statround[0] = statround[0] + 1
    #            else:
    #                #SQL query that creates the new record in case it isn't in the database
    #                #There is no need to use temporary variables because in the case of the INSERT query the VALUES are already handled in case they contain special characters
    #                dbcursor.execute(f'INSERT INTO publicusers (steamid, personaname, profileurl, avatar, avatarmedium, avatarfull, personastate, communityvisibilitystate, profilestate, lastlogoff, commentpermission) VALUES {dbinput}')
    #                statnew = statnew + 1
    #                statround[1] = statround[1] + 1
    #            time.sleep(0.05)
    #            print(f'UPDATES: {statround[0]}\t NEW ENTRIES: {statround[1]}\t PASS:{statround[2]}')
    #            db.commit()
    #            j = j + 1
    #        #We delete the data in idlist we already used
    #        for k in range(len(playerData["response"]["players"])):
    #            playerData["response"]["players"].pop(0)
    #            idlist.pop(0)
    #            k = k + 1
    #        
    ##End of script statistics
    #dbcursor.execute('SELECT COUNT(*) FROM publicusers')
    #dbfetch = dbcursor.fetchall()
    #print(f'\nThe number of rows in the database: {dbfetch[0][0]}')
    #print(f'The number of records updated: {statupdate}.\nThe number of new records: {statnew}.\nAnd the number of requests: {statnew+statupdate}.')
    #
            
            
            
            
            
            

        #Export the request as playerSummary.json
        #DEBUG ONLY
        #with open('playerSummary.json', 'w', encoding='utf-8') as f:
        #    json.dump(playerSummary.json(), f, ensure_ascii=False, indent=4)
        #if p1.is_alive() != True:
        #    v1 = idcount
        #    #time.sleep(0.5)
        #    p1.start()
        #    idcount = idcount + 1
        #    
        #elif p2.is_alive() != False:
        #    v2 = idcount
        #    time.sleep(0.5)
        #    p2.start()
        #    idcount = idcount + 1
        
        
    #p1.join()
    #p2.join()