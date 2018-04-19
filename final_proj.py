from secrets import sports_radar_key
import requests
import json
import sqlite3
import sys
import plotly.plotly as py
import plotly.graph_objs as go


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
                'Injury' TEXT,
                'Year' INTEGER
                ); '''

    cur.execute(statement)

    statement = '''  CREATE TABLE 'Roster' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Name'  TEXT,
                'NameId' INTEGER,
                'Position' TEXT
                ); '''

    cur.execute(statement)
    conn.commit()
    conn.close()

init_db()


possible_years = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']

year = input("Please select an NFL season between the years 2010 and 2017 or 'exit' to quit: ")

while year != 'exit':
    year = input("Please select an NFL season between the years 2010 and 2017 or 'exit' to quit: ")
    if year in possible_years:

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
                        player_info.append(year)
                    except:
                        body_part = 'None'
                        player_info.append(body_part)
                        player_info.append(year)
                    insert_lst_1.append(player_info)

            nfl_official_url_2009 = (base_url + "/nfl-ot2/seasontd/" + str(2009) + '/REG/' + str(num) + "/injuries.json?api_key=" + sports_radar_key)
            data = json.loads(make_request_using_cache(nfl_official_url_2009))

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
                        player_info.append(2009)
                    except:
                        body_part = 'None'
                        player_info.append(body_part)
                        player_info.append(2009)
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

                for position in team_defense:
                    player = position['position']['players']
                    for person in player:
                        person_lst = []
                        person_lst.append(person['name'])
                        person_lst.append(person['position'])
                        if person_lst not in insert_lst_2:
                            insert_lst_2.append(person_lst)
                        else:
                            continue

                for position in team_special_teams:
                    player = position['position']['players']
                    for person in player:
                        person_lst = []
                        person_lst.append(person['name'])
                        person_lst.append(person['position'])
                        if person_lst not in insert_lst_2:
                            insert_lst_2.append(person_lst)
                        else:
                            continue


        def insert_stuff():
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()

            for player in insert_lst_1:
                insertion = (None, player[0], player[1], player[2])
                statement = 'INSERT INTO "Injuries" '
                statement += 'VALUES (?, ?, ?, ?)'
                cur.execute(statement, insertion)

            players_dict = {}
            statement = 'SELECT Id, Name FROM Injuries'
            cur.execute(statement)
            for player in cur:
                players_dict[player[1]] = player[0]

            for player in insert_lst_2:
                if player[0] in players_dict:
                    insertion = (None, player[0], players_dict[player[0]], player[1])
                    statement = 'INSERT INTO "Roster" '
                    statement += 'VALUES (?, ?, ?, ?)'
                    cur.execute(statement, insertion)
                else:
                    insertion = (None, player[0], None, player[1])
                    statement = 'INSERT INTO "Roster" '
                    statement += 'VALUES (?, ?, ?, ?)'
                    cur.execute(statement, insertion)
            conn.commit()
            conn.close()

        insert_stuff()

        def total_injuries_by_year():
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()

            statement = 'SELECT Injury, Count(Injury), Year FROM Injuries WHERE Year <> 2009 Group By Injury Order By Count(injury) DESC'
            cur.execute(statement)

            injury_type = []
            injury_total = []

            for row in cur:
                injury_type.append(row[0])
                injury_total.append(row[1])

            data = [go.Bar(
                        x= injury_type,
                        y= injury_total
                )]

            py.plot(data, filename='injuries_in_year')

        # total_injuries_by_year()


        def concussions_by_year():
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()

            statement = " SELECT Count(Injury) FROM Injuries WHERE Injury = 'Concussion' and Year <> 2009 "
            cur.execute(statement)

            for row in cur:
                num_concussions = row[0]

            statement = " SELECT Count(Injury) FROM Injuries WHERE Year <> 2009 "
            cur.execute(statement)

            for row in cur:
                num_total_injuries = row[0]

            num_other_injuries = (num_total_injuries - num_concussions)
            labels = ['Concussions','Other Injuries']
            values = [num_concussions, num_other_injuries]
            trace = go.Pie(labels=labels, values=values)

            py.plot([trace], filename='concussion_percentage_in_year')

        # concussions_by_year()


        def injuries_by_position():
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()

            statement = ''' SELECT Position, Count(Injury), Year FROM Injuries JOIN Roster ON Injuries.Id = Roster.NameId
                        WHERE Year <> 2009  GROUP BY Position ORDER BY Count(Injury) DESC  '''

            cur.execute(statement)

            position_lst = []
            num_of_injuries_lst = []

            for row in cur:
                position_lst.append(row[0])
                num_of_injuries_lst.append(row[1])

            data = [go.Bar(
                        x= position_lst,
                        y= num_of_injuries_lst
                )]

            py.plot(data, filename='num_injuries_by_position')

        # injuries_by_position()

        def concussion_compared_to_2009():
            conn = sqlite3.connect(DBNAME)
            cur = conn.cursor()

            statement = ''' SELECT Count(Injury) FROM Injuries WHERE Injury = 'Concussion' and Year = 2009 '''
            cur.execute(statement)

            concussion_lst = []

            for row in cur:
                concussion_lst.append(row[0])

            statement = ''' SELECT Count(Injury) FROM Injuries WHERE Injury = 'Concussion' and Year <> 2009 '''
            cur.execute(statement)

            for row in cur:
                concussion_lst.append(row[0])

            data = [go.Bar(
                        x= ['2009', str(year)],
                        y= concussion_lst
                )]

            py.plot(data, filename='concussion_comparison')


        # concussion_compared_to_2009()

        print ( ' ')
        print('1. The total number of injuries in ' + year)
        print('2. The Percentage of concussions in ' + year)
        print('3. The total number of injuries by position in ' + year)
        print('4. The total number of concussions in ' + year + ' compared to 2009')
        print( ' ')

        more_info = input('Please input a number above display the information would you like to see for season ' + year + ': ')
        while more_info != 'exit':

            if more_info == '1':
                total_injuries_by_year()
            elif more_info == '2':
                concussions_by_year()
            elif more_info == '3':
                injuries_by_position()
            elif more_info == '4':
                concussion_compared_to_2009()
            else:
                print('Please enter a valid number')
            more_info = input('Please input a number above display the information would you like to see for season ' + year + ': ')

print('bye')
