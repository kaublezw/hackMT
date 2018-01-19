from flask import Flask, render_template, request, jsonify
from datetime import datetime
import sqlite3 as sql
app=Flask(__name__)

app.debug = True

@app.route('/')
def home():
    return  "Hello World"

@app.route('/controls')
def controls():
    return render_template('controls.html')

@app.route('/getCommand')
def getCommand():
   try:
      with sql.connect("//var//www//FlaskApps//HelloWorld//poc") as con:
         cur = con.cursor()
         cur.execute("SELECT command, updown, leftright, tofro FROM commands ORDER BY issued_date DESC LIMIT 1")
         rows = cur.fetchall()
         thecommand = {{}}
         if len(rows) > 0:
            for row in rows:
               thecommand["command"] = row["command"]
               thecommand["updown"] = row["updown"]
               thecommand["leftright"] = row["leftright"]
               thecommand["tofro"] = row["tofro"]
            cur.execute("DELETE FROM commands")
         else:
            thecommand["command"] = "none"
         return jsonify(thecommand)
   except:
#     raise
#     msg = "failed"
      con.rollback()
   finally:
#      return msg
      con.close()




#insert commands into database
@app.route('/issueCommand', methods=['POST'])
def issueCommand():
   try:
      c = request.form['command']
      updown = request.form['updown']
      leftright = request.form['leftright']
      tofro = request.form['tofro']

      with sql.connect("//var//www//FlaskApps//HelloWorld//poc") as con:
         cur = con.cursor()
         cur.execute("INSERT INTO commands(command,updown,leftright,tofro, issued_date) VALUES(?,?,?,?,?)",
            (c,updown,leftright,tofro,datetime.today()))
         con.commit()
         else:
            thecommand["command"] = "none"
         return jsonify(thecommand)
   except:
#     raise
#     msg = "failed"
      con.rollback()
   finally:
#      return msg
      con.close()



if __name__ == "__main__":
   app.run(debug=True)
