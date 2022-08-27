from datetime import datetime
import imp
from time import sleep
from flask import Flask,request,make_response
from json import loads, dumps
from waitress import serve
import sqlite3
import pandas as pd
import requests

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

######### HELPERS #########

def addTeam(name, description, cId, year):
    return

def addMatchResults(cId, homeId, guestId, winnerId, homeScore, guestScore, homePwd, guestPwd):
    success = False
    msg = ""
    if cId and homeId and guestId and homePwd and guestPwd:
        success = True
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
    df = pd.read_sql_query("SELECT * from teams", conn)
    teams = df.to_dict('records')

    return teams

def getScoreboard():
    return

if __name__ == "__main__":
    # serve(app, listen='*:7887', threads=1)

    # make http request with proxy
    for i in range(20, 250):
        print(i)
        proxies = {
            'http': f'http://192.168.20.101:{10000+i}',
            'https': f'http://192.168.20.101:{10000+i}',
        }
        try:
            r = requests.get('https://www.pureeconomy.de', proxies=proxies)
            print(r.text)
        except Exception as e:
            print(e)
            continue
        
        print(datetime.now())
        sleep(1)
