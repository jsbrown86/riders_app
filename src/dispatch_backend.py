"""
backend.py

Author:       Jacob Brown

Last Updated: Apr 22, 2016

This program is responsible for the functionality of the SafeRide App by the
Riders (myself, Conor, Zhibin). Depends on an input validation program and
map validation program by Conor Tracey.

"""

from flask import Flask, render_template, request
import sqlite3 as sql
from input_val import *
from Map_util import *
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

app = Flask(__name__)
GoogleMaps(app)

# Simple routes to various pages
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/enternew')
def new_request():
    return render_template('reserve.html')

@app.route('/showLogin')
def showLogin():
    return render_template('login.html')

@app.route('/showCancel')
def cancel():
    return render_template('cancel.html')

@app.route('/toHome')
def toHome():
    return render_template('index.html')

@app.route('/showReserve')
def showReserve():
    return render_template('reserve.html')

# This is used for the dispatch login page - anything other than the username
# and password described below will route the user to a login failure page.
# Otherwise, they'll be routed to a login success page, which will bring them
# to the dispatch page.
@app.route('/submitty', methods = ['POST', 'GET'])
def submitty():
    if request.method == 'POST':
        user = request.form['inputUser']
        pw = request.form['inputPW']
        if user == 'admin' and pw == 'pw':
            login_msg = 'Login successful!'
            return render_template('dispatch_login_success.html', login_msg = login_msg)
        else:
            login_msg = 'Login failure - redirecting back...'
        return render_template('dispatch_login_failure.html', login_msg = login_msg)
    return render_template('dispatch_login_results.html', login_msg = login_msg)

# This accepts a request by the user and decides if it's usable (i.e., it's
# within the correct boundaries, the student ID number is in the valid
# format, the student ID is unique and not already in our active database).
# Then it routes them to the map display page with the appropriate message.
@app.route('/rider',methods = ['POST', 'GET'])
def rider():
    thing = "Invalid request"
    msg = "Request already submitted"
    if request.method == 'POST':
        try:
            nm = request.form['inputName']
            tm = request.form['inputTime']
            phn = request.form['inputPhone']
            uoid = request.form['inputID']
            tddr = request.form['inputTo']
            fddr = request.form['inputFrom']
            rdrs = request.form.get('inputRiders')
            cmts = request.form['inputComment']

            bad = False
            my_map = ''

            if (Is_In_Bounds(tddr)==False) or (Is_In_Bounds(fddr) == False):
                bad = True

            if (Id_is_Valid(uoid)) == False:
                bad = True

            if bad:
                thing = "Invalid request"
                msg =  "Please check the addresses or student ID submitted"

            else:
                pickup = Address_to_Long_Lat(fddr)
                dropoff = Address_to_Long_Lat(tddr)

                my_map = make_map(pickup[0], pickup[1], dropoff[0], dropoff[1])
                

                with sql.connect("database.db") as con:
                    cur = con.cursor()

                    cur.execute("INSERT INTO requests (name,time,phone,uo_id,to_addr,from_addr,riders,active,comments) VALUES (?,?,?,?,?,?,?,'Yes',?)",(nm,tm,phn,uoid,tddr,fddr,rdrs,cmts) )
                
                    con.commit()
                thing = "Request submitted"
                msg = "If we are unable to fulfill your request, a dispatcher will call you at the number submitted"
        except:
                oon.rollback()
                msg = "Error in submitting request"

        finally:
                return render_template("map.html",msg = msg,thing=thing, my_map=my_map)
                con.close()

# This controls some of the functionality of the dispatcher page. It returns
# each entry row-by-row from the database, determines if an entry is to be
# set to "inactive", and if the database is to be cleared.
@app.route('/dispatch_display', methods=['POST', 'GET'])
def dispatch():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from requests where active == 'Yes' order by time ")

    rows = cur.fetchall()
    
    bad_app = request.form.get('bad_input', default=False, type=bool)
    thing = ""
    
    if request.method == 'POST':
        if request.form['submit'] == "Clear Database":
            con = sql.connect("database.db")
            cur = con.cursor()

            cur.execute("DELETE FROM requests")
            con.commit()
            con.close()

            return render_template("dispatch_results.html",rows = rows, thing=thing)

        else:
            
            name_app = request.form['name_input']
            id_app = request.form['id_input']
            
            con = sql.connect("database.db")
            cur = con.cursor()

            cur.execute("update requests set active = 'No' where uo_id = ?", [id_app])
            con.commit()
            con.close
            
            if bad_app == True:
                try:
                    con = sql.connect("master.db")
                    cur = con.cursor()
                                
                    cur.execute("INSERT INTO mdb (uoid) VALUES (?)", [id_app] )
                                
                    con.commit()

                except:
                    oon.rollback()
                    thing = "Error in adding to bad database"
                
                finally:
                    return render_template("dispatch_results.html",rows = rows,name_app = name_app, thing=thing)

            return render_template("dispatch_results.html",rows = rows,name_app = name_app, thing=thing)
    return render_template("dispatch_display.html",rows = rows, thing = thing)

if __name__ == '__main__':
    app.run(debug = True)
