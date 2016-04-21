from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/enternew')
def new_request():
    return render_template("reserve.html")

@app.route('/rider',methods = ['POST', 'GET'])
def rider():
    if request.method == 'POST':
        try:
            nm = request.form['inputName']
            tm = request.form['inputTime']
            phn = request.form['inputPhone']
            uoid = request.form['inputID']
            tddr = request.form['inputTo']
            fddr = request.form['inputFrom']
            rdrs = request.form['riders']
            cmts = request.form['inputComment']

            with sql.connect("database.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO requests (name,time,phone,uo_id,to_addr,from_addr,riders,active,comments) VALUES (?,?,?,?,?,?,?,'Yes',?)",(nm,tm,phn,uoid,tddr,fddr,rdrs,cmts) )
            
                con.commit()
                msg = "Record successfully added"
        except:
                oon.rollback()
                msg = "Error in submitting request - are one of the fields empty?"

        finally:
                return render_template("map.html",msg = msg)
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
