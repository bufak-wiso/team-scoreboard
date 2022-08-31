from flask import Flask,request,make_response, redirect
from json import loads, dumps
from waitress import serve
import sqlite3
import pandas as pd

DB_FILENAME = "test.db"
app = Flask(__name__)
conn = sqlite3.connect(DB_FILENAME, check_same_thread=False)

# @app.before_request
# def before_request():
#     if not request.is_secure:
#         url = request.url.replace('http://', 'https://', 1)
#         code = 301
#         return redirect(url, code=code)

@app.teardown_request
def teardown_request_func(f):

    log_arg = request.args.get('log')

    # check if logging is disabled via argument
    if log_arg and log_arg.lower() == "false":
        enable_log = False
    else:
        enable_log = True

    # when logging enabled: hand down if exception is present
    if enable_log:
        if f: # f is the error
            exception = True
        else:
            exception = False

@app.route("/")
def ServerMessage():
    return "This is your favorite drinking game scoreboard api!" 

@app.route("/version")
def myrequest():
    r = 'WIP, stay tuned!'
    return r

# Accepts new match results
# Example POST Data: {"cId": 1, "homeId": 23, "guestId": 3, "winnerId": 3, "homeScore": 0, "guestScore": 1, "homePwd": "fsr4ever", "guestPwd": "kekbert"}
# Example Response: {"success": true, "msg": "Match results successfully added!"}
@app.route("/add-match", methods=['POST'] )
def add_match_handler():
    request_data = loads(request.data.decode())
    response_data = {}
    try:
        cId = int(request_data.get("cId"))
        homeId = int(request_data.get("homeId"))
        guestId = int(request_data.get("guestId"))
        winnerId = int(request_data.get("winnerId"))
        homeScore = int(request_data.get("homeScore", 1 if homeId == winnerId else 0))
        guestScore = int(request_data.get("guestScore", 1 if guestId == winnerId else 0))
        homePwd = request_data.get("homePwd")
        guestPwd = request_data.get("guestPwd")

        success, msg = addMatchResults(cId, homeId, guestId, winnerId, homeScore, guestScore, homePwd, guestPwd)
        response_data = {"success": success, "msg": msg}
    except Exception as e:
        response_data = {"success": False, "msg": "Error: " + str(e)}

    body = dumps(response_data)
    resp = make_response(body)
    resp.headers["Access-Control-Allow-Origin"] = "*" # allow all origins (esp. for firefox cors problems)
    return resp

# Gets all team data
# Example Response Data: {"teams": [{"tId": 1, "name": "FC Suffenhausen", "description": "Nur der BVB!", "cId": 1, "year": "2022"}, {"tId": 2, "name": "1.FC Partyborn", "description": "Partyborn, Junge!", "cId": 1, "year": "2022"}, {"tId": 3, "name": "Bufak Allstars", "description": "Wir wissen, wo es l\u00e4uft!", "cId": 2, "year": "2022"}, {"tId": 4, "name": "Pong zur Bong", "description": "420", "cId": 2, "year": "2022"}]}
@app.route("/get-teams", methods=['GET'] )
def get_teams_handler():
    response_data = {}

    cId = request.args.get('cId', default = 0, type = int)
    teams = getTeams(cId)
    response_data = {"teams": teams}

    body = dumps(response_data)
    resp = make_response(body)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

# Example Request Data: {"name": "FC Teststadt", "description": "Wer sind wir? Egal!", "cId": 1, "year": "2022", "pwd": "666"}
# Example Response Data: {"success": true, "msg": "Team successfully added!"}
@app.route("/add-team", methods=['POST'] )
def add_team_handler():

    request_data = loads(request.data.decode(encoding="utf-8"))
    response_data = {}
    
    name = request_data.get("name")
    description = request_data.get("description")
    cId = request_data.get("cId")
    year = request_data.get("year")
    pwd = request_data.get("pwd")

    success, msg = addTeam(name, description, cId, year, pwd)
    response_data = {"success": success, "msg": msg}

    body = dumps(response_data)
    resp = make_response(body)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

@app.route("/get-scoreboard", methods=['GET'] )
def get_scoreboard_handler():
    response_data = {}
    
    cId = request.args.get('category')

    response_data = getScoreboard(cId)

    body = dumps(response_data)
    resp = make_response(body)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


######### HELPERS #########

def addTeam(name, description, cId, year, pwd):
    success = False
    msg = ""
    try:
        # add data to db with pandas dataframe
        df = pd.DataFrame({"tId": [None], "name": [name], "description": [description], "cId": [cId], "pwd": [pwd], "year": [year]})
        df.to_sql('teams', conn, if_exists='append', index=False)
        success = True
        msg = "Team successfully added!"
    except Exception as e:
        msg = "Error: " + str(e)
    return success, msg

def addMatchResults(cId, homeId, guestId, winnerId, homeScore, guestScore, homePwd, guestPwd):
    success = False
    msg = ""
    if cId and homeId and guestId and homePwd and guestPwd:

        # check if correct password
        # read password from db and compare with given password
        cur = conn.cursor()
        try:
            cur.execute("SELECT pwd FROM teams WHERE tid=?", (homeId,))
            homePwd_db = cur.fetchone()[0]
        except:
            return False, "Error: No team with tId " + str(homeId) + " found!"
        try:
            cur.execute("SELECT pwd FROM teams WHERE tid=?", (guestId,))
            guestPwd_db = cur.fetchone()[0]
        except:
            return False, "Error: No team with tId " + str(guestId) + " found!"
        cur.close()

        if homePwd == homePwd_db:
            if guestPwd == guestPwd_db:

                # add match results to db

                # old school approach
                # conn.execute(f'''INSERT INTO TABLE matches
                #         (mId, cId, homeId, guestId, homeScore, guestScore, winnerId, timestamp)
                #         VALUES (NULL, {cId}, {homeId}, {guestId}, {homeScore}, {guestScore}, {winnerId}, CURRENT_TIMESTAMP)''')
                # conn.commit()
                
                # new school approach   
                data=pd.DataFrame({"mId": [None], "cId": [cId], "homeId": [homeId], "guestId": [guestId], "winnerId": [winnerId], "homeScore": [homeScore], "guestScore": [guestScore]})
                data.to_sql('matches', con = conn, if_exists = 'append', index=False)

                success = True
            else:
                msg = "Error: Wrong guest team password!"
        else:
            msg = "Error: Wrong home team password!"
    
    return success, msg

def getTeams(cId):
    teams = []
   
    # # Alternative Manual
    # cur = conn.cursor()
    # cur.execute("SELECT * FROM teams")    # cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))
    # rows = cur.fetchall()
    # for row in rows:
    #     print(row)
    #     tid = row[0]
    #     name = row[1]
    #     description = row[2]
    #     cid = row[3]
    #     pwd = row[4]
    #     year = row[5]
    #     teams.append({"tid": tid, "name": name, "description": description, "cid": cid, "pwd": pwd, "year": year})
    # cur.close()

    # Alternative with Pandas (Python-Love! *-*)
    df = pd.read_sql_query("SELECT tId, name, description, cId, year from teams", conn).sort_values(by=["name"], ascending=True)
    
    # filter by category
    if cId != 0:
        df = df[df["cId"] == cId]
    teams = df.to_dict('records')
    return teams

def getScoreboard(category=1):
    '''
    This function retrieves all the match data from the db and creates a sorted pandas df scoreboard showing only teams with a minimum of 5 completed matches 
    '''
    MIN_COMPLETED_MATCHES = 1
    df_matches = pd.read_sql_query(f"SELECT * from matches where cId={category}", conn)#, index_col="mId")
    df_teams = pd.read_sql_query(f"SELECT * from teams where cId={category}", conn)#, index_col="mId")
    df_wins_per_team = df_matches.groupby('winnerId').agg({"winnerId": "count"})
    df_wins_per_team.columns = ["wins"]
    df_matches_per_team = pd.DataFrame(df_matches[["homeId", "guestId"]].stack().value_counts())
    df_matches_per_team.columns = ["matches"]
    df_matches_per_team_cleaned = df_matches_per_team[df_matches_per_team["matches"] > MIN_COMPLETED_MATCHES]
    list_of_relevant_teams = df_matches_per_team_cleaned.index.values.tolist()
    df_wins_per_team_cleaned = df_wins_per_team[df_wins_per_team.index.isin(list_of_relevant_teams)]
    df_wins_per_team_cleaned.rename(columns={"winnerId": "tId", "winnerId": "wins"}, inplace=True)

    scoreboard = df_wins_per_team_cleaned.join(df_matches_per_team)
    scoreboard["W/L ratio"]= scoreboard["wins"] / scoreboard["matches"]
    scoreboard.sort_values(by=["W/L ratio", "wins", "matches"], ascending=False, inplace=True)
    scoreboard = pd.merge(df_teams[["tId", "name"]], scoreboard, how='right', left_on='tId', right_on = 'winnerId')
    scoreboard.drop('tId', axis=1, inplace=True)
    print("Loaded match data from db.")
    # scoreboard = df.to_dict('records')
    return scoreboard.to_dict('records')

if __name__ == "__main__":
    # run flask app with ssl context
    context = ("./certs/cert.pem", "./certs/key.pem")
    app.run(host="0.0.0.0", port=7887, ssl_context="adhoc")
    # serve(app, listen='*:7887', threads=1)