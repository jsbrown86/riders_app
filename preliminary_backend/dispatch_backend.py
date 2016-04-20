from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('portal.html')

@app.route('/enternew')
def new_request():
    return render_template("rider_display.html")

@app.route('/rider',methods = ['POST', 'GET'])
def rider():
    if request.method == 'POST':
        try:
            nm = request.form['name']
            tm = request.form['time']
            phn = request.form['phone']
            uoid = request.form['uo_id']
            tddr = request.form['to_addr']
            fddr = request.form['from_addr']
            rdrs = request.form['riders']
            cmts = request.form['comments']

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
    cur.execute("select * from requests order by time")

    rows = cur.fetchall()
    con.close()
    
    if request.method == 'POST':
        try:
            name_app = request.form['name_input']
            thing = name_app
            
            con2 = sql.connect("master.db")
            cur2 = con2.cursor()

            
            con2.commit()
        except:

            thing = "whoops"
        finally:
            return render_template("dispatch_display.html",rows = rows,name_app = name_app, thing=thing)
                    
    
    return render_template("dispatch_display.html",rows = rows)

if __name__ == '__main__':
    app.run(debug = True)
