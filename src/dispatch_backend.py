from flask import Flask, render_template, request
import sqlite3 as sql
from input_val import *
from Map_util import *
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

app = Flask(__name__)
GoogleMaps(app)

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

@app.route('/submitty', methods = ['POST', 'GET'])
def submitty():
    if request.method == 'POST':
        user = request.form['inputUser']
        pw = request.form['inputPW']
        if user == 'admin' and pw == 'pw':
            login_msg = 'Login successful!'
        else:
            login_msg = 'Login failure'
        return render_template('dispatch_login_results.html', login_msg = login_msg)
    return render_template('dispatch_login_results.html', login_msg = login_msg)
        
@app.route('/rider',methods = ['POST', 'GET'])
def rider():
    msg = "eh"
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
            thing = ''
            #failure_1 = ''
            #failure_2 = ''
            my_map = ''

            if (Is_In_Bounds(tddr)==False) or (Is_In_Bounds(fddr) == False):
                #failure_1 = "INPUT ERROR: One or both of the addresses you entered is outside Safe Ride's Boundaries"
                bad = True

            if (Id_is_Valid(uoid)) == False:
                #failure_2 = "INPUT ERROR: The UO ID you entered is not valid"
                bad = True

            if bad:
                thing = "UH-OH, you dun entered the information wrong, asshole"

            else:
                pickup = Address_to_Long_Lat(fddr)
                dropoff = Address_to_Long_Lat(tddr)

                my_map = make_map(pickup[0], pickup[1], dropoff[0], dropoff[1])
                

            with sql.connect("database.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO requests (name,time,phone,uo_id,to_addr,from_addr,riders,active,comments) VALUES (?,?,?,?,?,?,?,'Yes',?)",(nm,tm,phn,uoid,tddr,fddr,rdrs,cmts) )
            
                con.commit()
                msg = "Record successfully added"
        except:
                oon.rollback()
                msg = "Error in submitting request - are one of the fields empty?"

        finally:
                return render_template("map.html",msg = msg,thing=thing, my_map=my_map)
                con.close()


@app.route('/dispatch_display', methods=['POST', 'GET'])
def dispatch():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from requests where active == 'Yes' order by time ")

    rows = cur.fetchall()

    con = sql.connect("master.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from mdb")
    rows2 = cur.fetchall()
    
    bad_app = request.form.get('bad_input', default=False, type=bool)
    thing = "Initial thing"
    
    if request.method == 'POST':
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
                thing = "Something went wrong"
            
            finally:
                return render_template("dispatch_results.html",rows = rows,name_app = name_app, thing=thing, rows2=rows2)

        return render_template("dispatch_results.html",rows = rows,name_app = name_app, thing=thing, rows2=rows2)
    return render_template("dispatch_display.html",rows = rows, rows2=rows2,thing = thing)

if __name__ == '__main__':
    app.run(debug = True)
