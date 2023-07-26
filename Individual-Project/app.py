
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
config = {
  "apiKey": "AIzaSyDk_5qb1lC4Tha2RSqwOIVDfwY33CzmHa4",
  "authDomain": "camels2.firebaseapp.com",
  "projectId": "camels2",
  "storageBucket": "camels2.appspot.com",
  "messagingSenderId": "1087414421140",
  "appId": "1:1087414421140:web:6c4c695f5550746a065681",
  "databaseURL":"https://camels2-default-rtdb.europe-west1.firebasedatabase.app/"
}

app = Flask(__name__,template_folder="templates",static_folder="static")
app.config['SECRET_KEY'] = 'super-secret-key'
firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db = firebase.database()



@app.route('/', methods=['GET', 'POST'])
def open_page():
        return render_template("home.html")




@app.route('/signin', methods=['GET', 'POST'])
def signin():   
    if request.method=="POST":
        email= request.form["email"]
        password= request.form["password"]
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))

        except Exception as e:
            print("SIGN IN ERROR:", e)
            error = "Authentication failed"
    return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
        error = ""   
        if request.method=="POST":
            email= request.form["email"]
            password= request.form["password"]
            name= request.form["name"]
            username= request.form["username"]
            bio= request.form["bio"]
            try:
                login_session['user'] = auth.create_user_with_email_and_password(email, password)
                UID = login_session['user']['localId']
                user = {"name": name, "email": email, "username":username,"bio":bio}
                db.child("Users").child(UID).set(user)
                return redirect(url_for('signin'))
            except:
                error = "Authentication failed"
                return render_template("signin.html")

        return render_template("signup.html")

@app.route('/', methods=['GET', 'POST'])
def home():
        return render_template("home.html")

@app.route('/adopt', methods=['GET', 'POST'])
def adopt():
        return render_template("adopt.html")



@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method =="POST":
        text= request.form["text"]
        image= request.form["image"]
        try:
            print("hello")
            print("LOGIN SESSION:", login_session)
            UID = login_session['user']['localId']
            post= {"image": image, "text":text, "uid": UID}
            print("POST::::::", post)
            db.child("posts").push(post)
            return redirect(url_for('posts'))
        except Exception as e:
            print('add POST EXCEPTION:', e)
            error = "Authentication failed"
    return render_template("add_post.html")


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    posts=db.child("posts").get().val()
    return render_template("posts.html", posts=posts)

@app.route('/logout')
def logout():
    login_session['user'] = None
    auth.current_user=None
    return redirect(url_for('home'))

@app.route('/sandy', methods=['GET', 'POST'])
def sandy():
    return render_template("sandy.html")

@app.route('/oscar', methods=['GET', 'POST'])
def oscar():
    return render_template("oscar.html")

@app.route('/lucky', methods=['GET', 'POST'])
def lucky():
    return render_template("lucky.html")

@app.route('/rex', methods=['GET', 'POST'])
def rex():
    return render_template("rex.html")

@app.route('/daisy', methods=['GET', 'POST'])
def daisy():
    return render_template("daisy.html")













           


#Code goes above here
if __name__ == '__main__':
    app.run(debug=True, port=5001)