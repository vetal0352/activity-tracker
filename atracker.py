import sqlite3
from datetime import datetime
from flask import Flask, session, request, g, redirect, render_template, flash, url_for

#configuration
DATABASE = 'atracker.db'
SECRET_KEY = 'just a very simple development key for wise-engineering.com'

app = Flask(__name__)
app.config.from_object(__name__)

def format_duration(minutes):
	if minutes > 59:
		return "{0} h {1} m".format(minutes // 60, minutes % 60) 
	else:
		return "{0} minutes".format(minutes)

def connect_db():
	return sqlite3.connect(app.config["DATABASE"])

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	g.db.close()

@app.route("/", methods=["GET", "POST"])
def index():
	
	if request.method == "POST":
	    g.db.execute("insert into activity (start_time, finish_time, distance, activity_type) values (?, ?, ?, ?)",
                 [request.form["start-time"], request.form["finish-time"], request.form["distance"], request.form["activity-type"]])
	    g.db.commit()
	    # flash("New activity was successfully saved")

	cur = g.db.execute("select activity_date, activity_type, distance, ((strftime('%s', finish_time) - strftime('%s', start_time)) / 60) from activity order by id")
	activities = [dict(	adate=datetime.strptime(row[0], "%Y-%m-%d").strftime("%B %d"), 
						type=row[1], 
						distance=row[2], 
						duration=format_duration(row[3]), 
						speed=round(row[2] / (row[3] / 60), 1)) for row in cur.fetchall()]

	cur = g.db.execute("select activity_date, activity_type, max(distance), ((strftime('%s', finish_time) - strftime('%s', start_time)) / 60) from activity group by activity_type")
	longest = 	[dict(	adate=datetime.strptime(row[0], "%Y-%m-%d").strftime("%b %d"), 
						type=row[1], 
						distance=row[2], 
						duration=format_duration(row[3])) for row in cur.fetchall()]
	    
	cur = g.db.execute("select activity_type, sum(distance) from activity group by activity_type")
	total = 	[dict(	type=row[0], 
						distance=row[1]) for row in cur.fetchall()]
		
	return render_template("activity-tracker.html", activities=activities, longest=longest, total=total)	
