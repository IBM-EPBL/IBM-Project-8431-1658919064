from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import json
import requests
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32731;PROTOCOL=TCPIP;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=mbd73622;PWD=DxrsqQuuiC8JEIN1",'','')
app = Flask(__name__)
@app.route('/registration')
def home():
    return render_template('register.html')

@app.route('/register',methods=['POST'])
def register():
    
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    city = request.form['city']
    infect = request.form['infect']
    blood = request.form['blood']
    password = request.form['passw']
    print(name,email,phone,city,infect,blood,password)
   

    try:
        sql = "SELECT * FROM plasmadonor WHERE email ='"+email+"'"
        # stmt = ibm_db.prepare(conn, sql)
        stmt = ibm_db.exec_immediate(conn,sql)
        print(ibm_db.num_rows(stmt))
        print("Ck1")
        # ibm_db.bind_param(stmt,1,email)
        print("Ck2")
        # ibm_db.execute(stmt)
        print("Ck3")
        # account = ibm_db.fetch_assoc(stmt)
        print(stmt)
        if  ibm_db.num_rows(stmt)>=0:
            return render_template('register.html', pred="You are already a member, please login using your details")
            # return "if block"
        else:
            print("else block")
            sql = "INSERT INTO plasmadonor (name,email,phone,city,infect,blood,password) VALUES ('"+name+"','"+email+"','" +phone+"','"+ city+"','"+ infect+"','"+blood+"','"+password+"')"
            print(sql)
            stmt = ibm_db.exec_immediate(conn,sql)
            print(ibm_db.num_rows(stmt))
            print(stmt)
            print("CK1 in else")
            # return "ELse block updated"
            return render_template('login.html', pred="Registration Successful, please login using your details")
    except Exception as e:
        print(e)
        return "error"
    return "success"
@app.route("/about")      
def about_page():
    return render_template('about.html')
        
@app.route('/')    
@app.route('/login')
def login():
    return render_template('login.html')
    
@app.route('/loginpage',methods=['POST'])
def loginpage():
    # data = request.get_json()
    # print(data)
    mail = request.form['user']
    # mail = data['email']
    # passw = data['password']
    passw=request.form['passw']
    sql = "SELECT * FROM plasmadonor WHERE email='"+mail+"'"+"AND password='"+passw+"'"
    print(sql)
    stmt = ibm_db.exec_immediate(conn,sql)
    print(ibm_db.num_rows(stmt))
    # account = ibm_db.fetch_assoc(stmt)
    print (stmt)
    result = ibm_db.fetch_both(stmt)
    # print(user,passw)
    if len(result)>0:
            print(result)
            return redirect(url_for('status'))           
            # return "Login Successfully"
    else:
        print(result)
        # return "Unsuccessfully"
        return render_template('login.html', pred="Login unsuccessful. Incorrect username / password !") 
      
        
@app.route('/status')
def status():
    sql = "SELECT count(blood) FROM plasmadonor group by blood "
    stmt = ibm_db.exec_immediate(conn, sql)
    count = ibm_db.num_rows(stmt)
    
    return render_template('status.html',b=25,b1=5,b2=3,b3=2,b4=2,b5=3,b6=3,b7=2,b8=5)
@app.route('/requester')
def requester():
    return render_template('request.html')


@app.route('/requested',methods=['POST'])
def requested():
    bloodgrp = request.form['bloodgrp']
    address = request.form['address']
    print(address)
    sql = "SELECT * FROM plasmadonor WHERE blood=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,bloodgrp)
    ibm_db.execute(stmt)
    data = ibm_db.fetch_assoc(stmt)
    msg = "Need Plasma of your blood group for: "+address
    while data != False:
        print ("The Phone is : ", data["PHONE"])
        url="https://www.fast2sms.com/dev/bulk?authorization=xCXuwWTzyjOD2ARd1EngbH3a7tKIq5PklJ8YSf0Lh4FQZecs9iNI1dSvuqprxFwCKYJXA5amQkBE36Rl&sender_id=FSTSMS&message="+msg+"&language=english&route=p&numbers="+str(data["PHONE"])
        result=requests.request("GET",url)
        print(result)
        data = ibm_db.fetch_assoc(stmt)
    return render_template('request.html', pred="Your request is sent to the concerned people.")
    

if __name__ == "__main__":
    app.run()

