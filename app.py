from flask import Flask,render_template,request,session,redirect,url_for,flash
import os
from werkzeug.utils import secure_filename
import mysql.connector
from flask_mysqldb import MySQL
app = Flask(__name__)

connection = mysql.connector.connect(host="localhost",user="root",password="",database="project")



mycursor = connection.cursor()
UPLOAD_FOLDER = os.path.join('static', 'upload')
ALLOWED_EXTENSIONS = {'mp4','png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# mycursor = connection.cursor()
# UPLOAD_FOLDER = os.path.join('static', 'upload')
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.secret_key = "hk"

@app.route("/")
def home():
    return render_template("/adminlogin.html")

   
@app.route("/index")
def index():
    return render_template('/index.html',UserName=session['UserName'])   


 
@app.route('/adminlogin',methods=['GET','POST'])
def login():
    msg=''
    if request.method=='POST':
        UserName = request.form['UserName']
        Password = request.form['Password']
        mycursor.execute('SELECT * FROM adminlogin WHERE UserName= %s AND Password= %s',(UserName,Password))
        record = mycursor.fetchone()
        if record:
            session['loggedin']= True
            session['UserName']= record[1]
            return redirect(url_for('index'))
        else:
            msg ='Incorrect UserName/Password.Try again' 
    return render_template('adminlogin.html',msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin',None)  
    session.pop('UserName',None)
    return redirect(url_for('login'))


app.secret_key = 'yk'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)



#------------plan--------------#


@app.route('/plan')
def plan():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM plan")
    data = cur.fetchall()
    cur.close()




    return render_template('plan.html', sqldata=data )



@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        pname= request.form['planname']
        pamount= request.form['planamount']
        pduration = request.form['planduration']
        cur = mysql.connection.cursor() 
        cur.execute("INSERT INTO plan (planname, planamount, planduration) VALUES (%s, %s, %s)", (pname, pamount, pduration))
        mysql.connection.commit()
        return redirect(url_for('plan'))




@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("Update plan set status='INACTIVE' WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('plan'))





@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        pname = request.form['planname']
        pamount = request.form['planamount']
        pduration = request.form['planduration']
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE plan
               SET planname=%s, planamount=%s, planduration=%s,status=%s
               WHERE id=%s
            """, (pname, pamount, pduration,status, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('plan'))



#-------------movie-----------#

@app.route('/movie')
def movie():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM movie m,category c,language l where m.category=c.C_id and m.language=l.L_id")
    data = cur.fetchall()
    print(data)

    cur.close()
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM category")
    cdata = cur.fetchall()
    cur.close()


    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM language")
    ldata = cur.fetchall()
    cur.close()

    return render_template('movie.html',  sqldata=data ,cdata=cdata,ldata=ldata)



@app.route('/insertt', methods = ['GET','POST'])
def insertt():

    if request.method == "POST":
       # Upload file flask
        uploaded_img = request.files['uploaded-file']
        uploaded_img1 = request.files['uploaded-file1']
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        img_filename1 = secure_filename(uploaded_img1.filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        uploaded_img1.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename1))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        session['uploaded_img_file_path1'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename1) 
        getName=request.form.get("moviename")
        # getCategory=request.form.get("category")
        getCategory=request.form.__getitem__("category")
        # getLanguages=request.form.get("language")
        getLanguages=request.form.__getitem__("language")
        # getUpload=request.form.get("uploaded-file")
        print(img_filename)


        flash("Data Inserted Successfully")
        # Mname = request.form['moviename']
        # Mcategory = request.form['category']
        # Mlanguage = request.form['language']
        # upload = request.form['upload']
        # cur = mysql.connection.cursor()
        # cur.execute("INSERT INTO movie (moviename, category, language,upload) VALUES (%s, %s, %s,%s)", (Mname, Mcategory, Mlanguage,upload))
        query ="INSERT INTO `movie`(`moviename`, `category`, `language`, `upload`,`image1`) VALUES  ("'%s'", "'%s'", "'%s'","'%s'","'%s'")"
        # data=(Mname,Mcategory,Mlanguage,img_filename)
        data=(getName,getCategory,getLanguages,img_filename,img_filename1)

        mycursor.execute(query,data)
        connection.commit()
        mysql.connection.commit()
        return redirect(url_for('movie'))




@app.route('/deletee/<string:id_data>', methods = ['GET'])
def deletee(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    # cur.execute("DELETE FROM movie WHERE id=%s", (id_data,))
    cur.execute("Update movie set status='INACTIVE' WHERE id=%s", (id_data,))

    mysql.connection.commit()
    return redirect(url_for('movie'))





@app.route('/updatee',methods=['POST','GET'])
def updatee():
    if request.method == 'POST':
        getMid = request.form['id']
        getName = request.form['moviename']
        getCategory = request.form.__getitem__('category')
        getLanguage = request.form.__getitem__('language')
        getstatus = request.form['status']
        video_original=request.form['video_original']
        getUpload = request.files['uploaded-file']
        uploaded_img1 = request.files['uploaded-file1']
        img_original1=request.form.get("img_original1")
        cur = mysql.connection.cursor()
        if getUpload.filename=='': 
            cur.execute("""
               UPDATE movie
               SET moviename=%s, category=%s, language=%s,Upload=%s, `image1`=%s,status=%s
               WHERE id=%s
            """,(getName, getCategory, getLanguage,video_original, img_original1,getstatus,getMid))
        else:
            
            uploaded_img = request.files['uploaded-file']
            img_filename = secure_filename(uploaded_img.filename)
            uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
            session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)

            uploaded_img1 = request.files['uploaded-file1']
            img_filename1 = secure_filename(uploaded_img1.filename)
            uploaded_img1.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename1))
            session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename1)

            cur.execute("""
               UPDATE movie
               SET moviename=%s, category=%s, language=%s,Upload=%s,  `image1`=%s,status=%s
               WHERE id=%s
            """,(getName, getCategory, getLanguage,img_filename,img_filename1,getstatus, getMid))

        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('movie'))


#---------------Category ----------#


@app.route('/category')
def category():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM category")
    data = cur.fetchall()
    cur.close()
    return render_template('category.html', sqldata=data )
    # category=db.execute("SELECT * FROM category order by Mcategory")
    # return render_template("category.html",sqldata=category )


@app.route('/inserttt', methods = ['POST'])
def inserttt():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        Mcategory= request.form['Mcategory']
        print(Mcategory)
        cur = mysql.connection.cursor() 
        query="INSERT INTO category (Mcategory) VALUES('" + Mcategory + "')"
        
        cur.execute(query)

        mysql.connection.commit()
        return redirect(url_for('category'))




@app.route('/deleteee/<string:id_data>', methods = ['GET'])
def deleteee(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("Update category set status='INACTIVE' WHERE C_id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('category'))





@app.route('/updateee',methods=['POST','GET'])
def updateee():

    if request.method == 'POST':
        mid = request.form['C_id']
        Mcategory = request.form['Mcategory']
       
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE category
               SET Mcategory=%s,status=%s
               WHERE C_id=%s
            """, (Mcategory,status,mid))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('category'))


#-------------language----------#

@app.route('/language')
def language():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM language")
    data = cur.fetchall()
    cur.close()
    return render_template('language.html', sqldata=data )
    # category=db.execute("SELECT * FROM category order by Mcategory")
    # return render_template("category.html",sqldata=category )


@app.route('/insertttt', methods = ['POST'])
def insertttt():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        Mlanguage= request.form['Mlanguage']
        
        cur = mysql.connection.cursor() 
        query="INSERT INTO language (Mlanguage) VALUES('" + Mlanguage + "')"
        
        cur.execute(query)
        mysql.connection.commit()
        return redirect(url_for('language'))




@app.route('/deleteeee/<string:id_data>', methods = ['GET'])
def deleteeee(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("Update language set status='INACTIVE' WHERE L_id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('language'))





@app.route('/updateeee',methods=['POST','GET'])
def updateeee():

    if request.method == 'POST':
        mid = request.form['L_id']
        Mlanguage = request.form['Mlanguage']
       
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE language
               SET Mlanguage=%s,status=%s
               WHERE L_id=%s
            """, (Mlanguage,status,mid))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('language'))



#-----customer-----#


@app.route("/buydet")
def buydet():
    
    query1 = "SELECT * FROM `buydetails`"
    mycursor.execute(query1)
    ldata=mycursor.fetchall()
     
    
     

    return render_template('/adplan.html', sqldata=ldata)

@app.route('/customer')
def customer():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM user_form")
    data = cur.fetchall()
    cur.close()
    return render_template('customer.html', sqldata=data )


@app.route('/deleteeeee/<string:id_data>', methods = ['GET'])
def deleteeeee(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("Update category set status='INACTIVE' WHERE C_id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('customer'))

    
@app.route('/updateeeee',methods=['POST','GET'])
def updateeeee():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['Name']
        email = request.form['Email']
        phoneno = request.form['PhoneNo']
        password = request.form['Password']
        dob = request.form['DOB']
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE user_form
               SET Name=%s, Email=%s, PhoneNo=%s,Password=%s,DOB=%s,status=%s
               WHERE id=%s
            """, (name, email, phoneno,password,dob,status, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('customer'))



#----UserLogin/SignUp----#

@app.route("/")
def uhome():
    return render_template("/adminlogin.html")

@app.route("/home1")
def userindex():
    return render_template('/home1.html')   

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
        return render_template("/signup.html" ,msg=msg)
 

@app.route('/login',methods=['GET','POST'])
def userlogin():
    msg=''
    if request.method=='POST':
        UserName = request.form['UserName']
        Password = request.form['Password']
        mycursor.execute('SELECT * FROM adminlogin WHERE UserName = %s AND Password= %s',(UserName,Password))
        record = mycursor.fetchone()
        if record:
            session['loggedin']= True
            session['UserName']= record[2]
            return render_template('index.html')
        else:
            msg ='Incorrect Email/Password.Try again' 
    return render_template('adminlogin.html',msg=msg)

if __name__ == "__main__":
    app.run(debug=True)
   











