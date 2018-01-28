from datetime import datetime
import sqlite3 as sql
import time

con = sql.connect("//var//www//FlaskApps//HelloWorld//poc")
cur = con.cursor()
    
def main():
            cur.execute("SELECT command, updown, leftright, tofro, issued_date, team FROM commands_queue WHERE command='Move'")
            allrows = cur.fetchall()
            if len(allrows) >0:
                team1rows = [x for x in allrows if x[5] == 1]
                team2rows = [x for x in allrows if x[5] == 2]
                processRows(team1rows)
                processRows(team2rows)
                cur.execute("DELETE FROM commands_queue")
                con.commit()
        
   



def processRows(rows):
    updown = sum(c[1] for c in rows)
    leftright = sum(c[2] for c in rows)
    tofro = sum(c[3] for c in rows)
    for row in rows:
        team = row[5]
        break
    

    if updown>0:
        updown = 1
    if updown<0:
        updown = -1
    if leftright>0:
        leftright = 1
    if leftright<0:
        leftright = -1
    if tofro>0:
        tofro = 1
    if tofro<0:
        tofro = -1
    cur.execute("INSERT INTO commands (command, updown, leftright, tofro, issued_date, team) VALUES ('Move',?,?,?,?,?)", (updown,leftright,tofro, datetime.today(), team,))

while True:
    main()
    time.sleep(.5)
