from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
import sqlite3 as sql

app=Flask(__name__)

app.debug = True

@app.route('/')
def home():
    return  "Hello World 2"

@app.route('/controls')
def controls():
    return render_template('controls.html')

@app.route('/controls2')
def controls2():
    return render_template('controls2.html')

@app.route('/blimpconfig')
def blimpconfig():
    return render_template('blimpconfig.html')

@app.route('/raceRegistration')
def raceRegistration():
    return render_template('raceRegistration.html')

@app.route('/registerUser', methods=['POST'])
def registerUser():
    with sql.connect("//var//www//FlaskApps//HelloWorld//poc") as con:
            name = request.form['name']
            raceid = request.form['raceid']
            token = os.urandom(12).encode('hex')
 
            cur = con.cursor()
            cur.execute("SELECT count(*) FROM players WHERE team = 1")
            row = cur.fetchone()
        
            team1count = row[0]
            cur.execute("SELECT count(*) FROM players WHERE team = 2")
            row = cur.fetchone()
            team2count = row[0]

            #Determines which team the player should be in
            #If noone in database, player is assigned team 1 automatically
            if team1count > team2count:
                team = 2
            else:
                team = 1
        
            cur.execute("INSERT INTO players (name, token, raceid, team) VALUES (?,?,?,?)", (name, token, raceid, team,))

            return token

@app.route('/getPlayers')
def getUsers():
    with sql.connect("//var//www//FlaskApps//HelloWorld//poc") as con:
        try:
            raceid = request.args.get('raceid')

            cur = con.cursor()
            cur.execute("SELECT * FROM players WHERE raceid = ?", (raceid,))
            rows = cur.fetchall()
            config = {}
            if len(rows) > 0:
                for row in rows:
                    config["team"] = row.team
                    config["name"] = row.name
            else:
                config["team"] = "none"
                config["name"] = "none"

            return jsonify(config)
        except:
            con.rollback()
            raise;
        finally:
            con.close() 

@app.route('/getConfig')
def getConfig():
    with sql.connect("//var//www//FlaskApps//HelloWorld//poc") as con:
            team = request.args.get('team')

            cur = con.cursor()
            cur.execute("SELECT team, trimupdown, trimleftright, upduration, leftrightduration, tofroduration, upspeed, tofrospeed, leftrightspeed FROM blimpconfig WHERE team = ?", (team,))
            row = cur.fetchone()
            config = {}
            if len(row) > 0:
                config["team"] = row[0]
                config["trimupdown"] = row[1]
                config["trimleftright"] = row[2]
                config["upduration"] = row[3]
                config["leftrightduration"] = row[4]
                config["tofroduration"] = row[5]
                config["upspeed"] = row[6]
                config["tofrospeed"] = row[7]
                config["leftrightspeed"] = row[8]
            else:
                config["team"] = team
                config["status"] = "no config found"

            return jsonify(config)
            con.close()      

@app.route('/getCommand')
def getCommand():
    with sql.connect("//var/www/FlaskApps//HelloWorld//poc") as con:
        
            team = request.args.get('team')

            cur = con.cursor()
            cur.execute("SELECT command, updown, leftright, tofro FROM commands WHERE team = ? ORDER BY issued_date DESC LIMIT 1", (team,))
            rows = cur.fetchall()
            thecommand = {}
            if len(rows) > 0:
                for row in rows:
                    #msg = "made it into row"
                    thecommand["command"] = row[0]
                    thecommand["updown"] = row[1]
                    thecommand["leftright"] = row[2]
                    thecommand["tofro"] = row[3]
                cur.execute("DELETE FROM commands")
            else:
                thecommand["command"] = "none"

            return jsonify(thecommand)
        
            con.close()
 
@app.route('/getCurrentRace')
def getCurrentRace():
   with sql.connect("//var//www//FlaskApps//HelloWorld//poc") as con:
        cur = con.cursor()
        cur.execute("SELECT rowid FROM race WHERE start_date is null AND stop_date is null ORDER BY start_date DESC LIMIT 1")
        row = cur.fetchone()
        thecommand = {}
        if row is None:
            thecommand["raceid"] = "none"
        else:
            thecommand["raceid"] = row[0]

        return jsonify(thecommand)
        

@app.route('/queueCommand', methods=['POST'])
def queueCommand():
    with sql.connect("//var//www//FlaskApps//HelloWorld//poc") as con:
        try:
            token = request.args.get('token')
            raceid = request.args.get('raceid')
    
    
            cur = con.cursor()
            cur.execute("SELECT * FROM players WHERE token = ? AND raceid = ?", (token, raceid)) 
            rows = cur.fetchall()
            if len(rows) > 0:
                c = request.form['command'] 
                updown = request.form['updown']
                leftright = request.form['leftright']
                tofro = request.form['tofro']
                cur.execute("INSERT INTO commands_queue(command,updown,leftright,tofro, issued_date) VALUES(?,?,?,?,?)", 
                    (c,updown,leftright,tofro,datetime.today()))  
                con.commit()
                msg = "record added"
        except: 
            msg = "failed"     
            con.rollback()
        finally:
            return  msg
            con.close()

#insert commands into database
@app.route('/issueCommand', methods=['POST'])
def issueCommand():
    with sql.connect("//var//www//FlaskApps//HelloWorld//poc") as con:
        try:
            token = request.form['token']
            team = request.form['team']

            cur = con.cursor()
            cur.execute("SELECT * FROM players WHERE token = ?", (token,)) 
            rows = cur.fetchall()
            if len(rows) > 0:
                c = request.form['command'] 
                updown = request.form['updown']
                leftright = request.form['leftright']
                tofro = request.form['tofro']
                cur.execute("INSERT INTO commands(command,updown,leftright,tofro, issued_date,team) VALUES(?,?,?,?,?,?)", 
                   (c,updown,leftright,tofro,datetime.today(), team,))  
                con.commit()
                msg = "record added"
        except: 
            msg = "failed"     
            con.rollback()
        finally:
            return  msg
            con.close()

@app.route('/updateBlimpConfig', methods=['POST'])
def updateBlimpConfig():
    with sql.connect("//var//www//FlaskApps//HelloWorld//poc") as con:
            cur = con.cursor()
            team = request.form['team']
            trimupdown = request.form['trimupdown']
            trimleftright = request.form['trimleftright']
            upduration = request.form['upduration']
            leftrightduration = request.form['leftrightduration']
            tofroduration = request.form['tofroduration']
            upspeed = request.form['upspeed']
            tofrospeed = request.form['tofrospeed']
            leftrightspeed = request.form['leftrightspeed']

            cur.execute("UPDATE blimpconfig SET trimupdown = ?, trimleftright = ?, upduration = ?, leftrightduration = ?,"
                        "tofroduration = ?, upspeed = ?, tofrospeed = ?, leftrightspeed = ? WHERE team = ?",
                        (trimupdown, trimleftright, upduration, leftrightduration, tofroduration, upspeed, tofrospeed, leftrightspeed,
                         team,))
	    return "success"
if __name__ == "__main__":
   app.run(debug=True)
