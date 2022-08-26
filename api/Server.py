from flask import Flask,request,make_response
from json import loads, dumps
from waitress import serve
import sqlite3
import pandas as pd

DB_FILENAME = "test.db"
app = Flask(__name__)
conn = sqlite3.connect(DB_FILENAME)

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
@app.route("/add-match", methods=['POST'] )
def add_match_handler():
    request_data = loads(request.data.decode())
    response_data = {}
    
    cId = request_data.get("cId")
    homeId = request_data.get("homeId")
    guestId = request_data.get("guestId")
    winnerId = request_data.get("winnerId")
    homeScore = request_data.get("homeScore", 1 if homeId == winnerId else 0)
    guestScore = request_data.get("guestScore", 1 if guestId == winnerId else 0)
    homePwd = request_data.get("homePwd")
    guestPwd = request_data.get("guestPwd")

    success, msg = addMatchResults(cId, homeId, guestId, winnerId, homeScore, guestScore, homePwd, guestPwd)
    response_data = {"success": success, "msg": msg}

    body = dumps(response_data)
    resp = make_response(body)
    resp.headers["Access-Control-Allow-Origin"] = "*" # allow all origins (esp. for firefox cors problems)
    return resp

# Gets all team data
# Example Response Data: 
@app.route("/get-teams", methods=['GET'] )
def get_teams_handler():
    response_data = {}
    teams = getTeams()
    response_data = {"teams": teams}

    body = dumps(response_data)
    resp = make_response(body)
    resp.headers["Access-Control-Allow-Origin"] = "*"

######### HELPERS #########

def addTeam(name, description, cId, year):
    return

def addMatchResults(cId, homeId, guestId, winnerId, homeScore, guestScore, homePwd, guestPwd):
    success = False
    msg = ""
    if cId and homeId and guestId and homePwd and guestPwd:

        # check if correct password
        # read password from db and compare with given password
        cur = conn.cursor()
        cur.execute("SELECT pwd FROM teams WHERE tid=?", (homeId,))
        homePwd_db = cur.fetchone()[0]
        cur.execute("SELECT pwd FROM teams WHERE tid=?", (guestId,))
        guestPwd_db = cur.fetchone()[0]
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
                data=pd.DataFrame({"mId": None, "cId": cId, "homeId": homeId, "guestId": guestId, "winnerId": winnerId, "homeScore": homeScore, "guestScore": guestScore})
                data.to_sql('matches', con = conn, if_exists = 'append')

                success = True
            else:
                msg = "Error: Wrong guest team password!"
        else:
            msg = "Error: Wrong home team password!"
    
    return success, msg

def getTeams():
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
    df = pd.read_sql_query("SELECT (tId, name, description, cId, year) from teams", conn)
    teams = df.to_dict('records')

    return teams

def getScoreboard():
    return

if __name__ == "__main__":
    conn = sqlite3.connect(DB_FILENAME)
    serve(app, listen='*:7887', threads=1)