from flask import Flask,render_template,request,session,redirect,url_for,flash
import os
from werkzeug.utils import secure_filename
import mysql.connector
from flask_mysqldb import MySQL
app = Flask(__name__)

connection = mysql.connector.connect(host="localhost",user="root",password="",database="project")



mycursor = connection.cursor()
UPLOAD_FOLDER = os.path.join('static')
ALLOWED_EXTENSIONS = {'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = "hk"

@app.route("/")
def home():
    return render_template("/login.html")

   
@app.route("/index")
def index():
    return render_template('/index.html',UserName=session['UserName'])   

@app.route('/logout')
def logout():
    session.pop('loggedin',None)  
    session.pop('UserName',None)
    return redirect(url_for('userlogin'))
 
# @app.route('/adminlogin',methods=['GET','POST'])
# def login():
#     msg=''
#     if request.method=='POST':
#         UserName = request.form['UserName']
#         Password = request.form['Password']
#         mycursor.execute('SELECT * FROM adminlogin WHERE UserName= %s AND Password= %s',(UserName,Password))
#         record = mycursor.fetchone()
#         if record:
#             session['loggedin']= True
#             session['UserName']= record[1]
#             return redirect(url_for('index'))
#         else:
#             msg ='Incorrect UserName/Password.Try again' 
#     return render_template('login.html',msg=msg)




app.secret_key = 'yk'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)



@app.route("/signup")
def s1():
    return render_template('/signup.html')  

@app.route("/signup",methods=["GET","POST"])
def valueread():
    msg=''
    if request.method=="POST":
        getName=request.form.get("Name")
        getEmail=request.form.get("Email")
        getPhoneNo=request.form.get("PhoneNo")
        getPassword=request.form.get("Password")
        getDOB=request.form.get("DOB")
        query =" INSERT INTO `user_form`( `Name`, `Email`, `PhoneNO`, `Password`,`DOB`) VALUES("'%s'", "'%s'", "'%s'","'%s'", "'%s'")"
        data=(getName,getEmail,getPhoneNo,getPassword,getDOB)
        print(getName)
        print(getEmail)
        print(getPhoneNo)
        print(getPassword)
        print(getDOB)
        mycursor.execute(query,data)
        connection.commit()
        msg ='You have successfully registered !'
        return redirect(url_for('userplan'))







#----UserLogin/SignUp----#

@app.route("/")
def uhome():
    
    return render_template("/login.html")

# @app.route("/test")
# def userindex():
#     return render_template('/test.html')   


 

@app.route('/login',methods=['GET','POST'])
def userlogin():
    msg=''
    if request.method=='POST':
        Email = request.form['Email']
        Password = request.form['Password']
        mycursor.execute('SELECT * FROM user_form WHERE Email= %s AND Password= %s',(Email,Password))
        record = mycursor.fetchone()
        if record:
            session['loggedin']= True
            session['Email']= record[1]
            session['id']= record[0]
            print(session['id'])
            return redirect(url_for('homeorg'))
        else:
            msg ='Incorrect Email/Password.Try again' 
    return render_template('login.html',msg=msg)









@app.route('/homeorg')
def homeorg():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `movie`")
    userdata = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM `language`")
    ldata = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM category")
    data = cur.fetchall()
    cur.close()


    return render_template('/home1.html', sqldata=userdata, lang=ldata ,cate=data   )  

    # -----------------------------catogory---------------
@app.route('/cl/<string:cl>')
def cl(cl):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM `movie` WHERE category=%s',(cl))
    data = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT  * FROM category WHERE `C_id`=%s',(cl))
    userdata = cur.fetchall()
    cur.close()
    return render_template('/cl1.html', sqldata=data,cl=userdata ) 
    # --------lang------------
@app.route('/ll/<string:ll>')
def ll(ll):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM `movie` WHERE `Language`=%s',(ll))
    data = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM `language` WHERE `L_id`=%s',(ll))
    userdata = cur.fetchall()
    cur.close()
    return render_template('/cl1.html', sqldata=data,cl=userdata ) 



@app.route('/category')
def category():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM category")
    data = cur.fetchall()
    cur.close()
    return render_template('/home1.html', cate=data )





@app.route('/play/<string:id>')
def play(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM `movie` where id="+id)
    userdata = cur.fetchall()
    cur.close()
    return render_template("/playvideo.html",sqldata=userdata)


#-------------------subscription-------------#
@app.route('/userplan')
def userplan():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM plan ")
    userdata = cur.fetchall()
    cur.close()




    return render_template('userplan.html', sqldata=userdata )  

@app.route('/viewplan/<string:plan>')
def viewplan(plan):
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM plan where id="+plan)
    plandata = cur.fetchall()
    cur.close()
    user=session['Email']
    print(user)
    # cur1 = mysql.connection.cursor()
    # cur1.execute('SELECT * FROM `user_form` WHERE `Name`=%s'(user,))
    # userdata = cur1.fetchall()
    # cur1.close()
    query1 = "SELECT * FROM `user_form` WHERE `Name`=%s"
    data=(user,)
    mycursor.execute(query1,data)
    userdata=mycursor.fetchall()
    return render_template("/view plan.html",userdata=userdata,sqldata=plandata)



@app.route("/buy",methods=["GET","POST"])
def buy():
    msg=''
    if request.method=="POST":
        getName=request.form.get("r1")
        getprice=request.form.get("r2")
        getmail=request.form.get("email")
       
        query =" INSERT INTO `buydetails`( `planname`, `price`, `user`) VALUES(%s,%s,%s)"
        data=(getName,getprice,getmail)
     
       
       
        mycursor.execute(query,data)
        connection.commit()
        msg ='You have successfully registered !'
        return redirect(url_for('homeorg'))

#-----------payment-----------#
@app.route('/payment/<string:plan>')
def payment(plan):
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM plan where id="+plan)
    userdata = cur.fetchall()
    cur.close()
    return render_template("/payment.html",sqldata=userdata)


#-----success----#
@app.route("/success/<string:pid>")
def getsuccess(pid):
    email=session['Email']  
    query1 = "UPDATE `user_form` SET `planid`=" + pid+" where `Email`='"+email+"'"
   
    mycursor.execute(query1)
    print(query1)
    return render_template("success.html")


 
if __name__ == "__main__":
    app.run(debug=True)
   