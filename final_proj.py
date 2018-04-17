from secrets import sports_radar_key
import requests
import json
import sqlite3
import sys

CACHE_FNAME = 'cache.json'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def get_unique_key(url):
    return url

def make_request_using_cache(url):
    unique_indent = get_unique_key(url)

    if unique_indent in CACHE_DICTION:
        return CACHE_DICTION[unique_indent]

    else:
        if "http://api.sportradar.us" in url:
            api_key = sports_radar_key
            resp = requests.get(url)
        else:
            resp = requests.get(url)
        CACHE_DICTION[unique_indent] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME, "w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_indent]

# Don't know if I need this
# def get_url(url):
#     return url

DBNAME = 'NFL.db'

def init_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement = '''
        DROP TABLE IF EXISTS 'Injuries';
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        DROP TABLE IF EXISTS 'Roster';
    '''

    cur.execute(statement)
    conn.commit()

    statement = '''  CREATE TABLE 'Injuries' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Name'  TEXT,
                'Injury' TEXT
                ); '''

    cur.execute(statement)


    statement = '''  CREATE TABLE 'Roster' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Name'  TEXT,
                'Position' TEXT
                ); '''

    cur.execute(statement)
    conn.close()

init_db()


year = 2015
all_weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

insert_lst_1 = []

for num in all_weeks:
    base_url = "http://api.sportradar.us"

    nfl_official_url = (base_url + "/nfl-ot2/seasontd/" + str(year) + '/REG/' + str(num) + "/injuries.json?api_key=" + sports_radar_key)
    data = json.loads(make_request_using_cache(nfl_official_url))

    teams= data['teams']
    week = data['week']['sequence']

    for team in teams:

        team_name = team['name']
        players = team['players']
        for player in players:
            player_info = []
            name = player['name']
            injuries = player['injuries'][0]
            player_info.append(name)
            try:
                body_part = injuries['primary']
                player_info.append(body_part)
            except:
                body_part = 'None'
                player_info.append(body_part)
            insert_lst_1.append(player_info)

# print(insert_lst_1)


insert_lst_2 = []

for num in all_weeks:
    base_url = "http://api.sportradar.us"

    nfl_official_url_2 = (base_url + "/nfl-ot2/seasontd/" + str(year) + '/REG/' + str(num) + "/depth_charts.json?api_key=" + sports_radar_key)
    data = json.loads(make_request_using_cache(nfl_official_url_2))

    teams= data['teams']

    for team in teams:
        team_offense = team['offense']
        team_defense = team['defense']
        team_special_teams = team['special_teams']
        for position in team_offense:
            player = position['position']['players']
            for person in player:
                person_lst = []
                person_lst.append(person['name'])
                person_lst.append(person['position'])
                if person_lst not in insert_lst_2:
                    insert_lst_2.append(person_lst)
                else:
                    continue

# print(insert_lst_2)


    # teams= data['teams']
    # week = data['week']['sequence']
    #
    # for team in teams:
    #
    #     team_name = team['name']
    #     # team_lst.append(team_name)
    #     players = team['players']
    #     for player in players:
    #         player_info = []
    #         name = player['name']
    #         injuries = player['injuries'][0]
    #         player_info.append(name)
    #         try:
    #             body_part = injuries['primary']
    #             player_info.append(body_part)
    #         except:
    #             body_part = 'None'
    #             player_info.append(body_part)
    #         insert_lst_1.append(player_info)

# print(name_lst)
# print(team_lst)
# print(week)
# print(injuries_lst)

# CREATING INJURY DICIONARY
# ------------------------------------
#     if body_part not in injury_dict:
#         injury_dict[body_part] = 1
#     else:
#         injury_dict[body_part] +=1
# except:
#     continue



def insert_stuff():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    for player in insert_lst_1:
        insertion = (None, player[0], player[1])
        statement = 'INSERT INTO "Injuries" '
        statement += 'VALUES (?, ?, ?)'
        cur.execute(statement, insertion)

    for player in insert_lst_2:
        insertion = (None, player[0], player[1])
        statement = 'INSERT INTO "Roster" '
        statement += 'VALUES (?, ?, ?)'
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()

insert_stuff()
