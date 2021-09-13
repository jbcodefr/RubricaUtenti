from flask import Flask,render_template,request, flash, redirect, url_for
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres@localhost/users'
db=SQLAlchemy(app)


class User(db.Model):
    __tablename__='utenti'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(150),unique=True)
    username=db.Column(db.String(150))
    password=db.Column(db.String(150))

def __init__(self,email,username,password):
    self.email=email
    self.username=username
    self.password=password

@app.route('/')
def home():
    userlist=User.query.all()
    return render_template("home.html",userlist=userlist)

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    uto = User.query.get_or_404(id)
    if request.method=='POST':
        email=request.form.get('email')
        username=request.form.get('username')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        
        if uto.email==request.form.get('email'):
            flash('Email already Used ',category='error') 
        elif len(email)<3:
            flash('_> Email > 4 charac',category='error')
        elif len(username)<2:
            flash('_> Username > 4 charac',category='error')
        elif password1!=password2:
            flash('_> password1!=password2',category='error') 
        elif len(password1)<2:
            flash('_> password > 5 charac',category='error')
        else:
            uto.email=request.form.get('email')
            uto.username=request.form.get('username')
            uto.password=generate_password_hash(request.form.get('password1'),method='sha256')
            db.session.commit()
            flash('User: "'+uto.username+'" Updated',category='success')
            ##login_user(user,remember=True)
            ## userResult=db.session.query(User)
            return redirect(url_for("home"))
    return render_template("update.html",user=uto)

@app.route('/delete/<int:id>',methods=['GET','POST'])
def delete_user(id):
        utd = User.query.get_or_404(id)
        username = utd.username
        if utd:
            db.session.delete(utd)
            db.session.commit()
            flash('User: "'+username+'" deleted',category='warning')
            return redirect(url_for("home")) 


@app.route('/signup',methods=['GET','POST'])
def sign_up(): 
    if request.method=='POST':
        email=request.form.get('email')
        username=request.form.get('username')
        password1=request.form.get('password1')
        password2=request.form.get('password2')

        user=User.query.filter_by(email=email).first()
        if user:
            flash('Email already Used ',category='error') 
        elif len(email)<3:
            flash('_> Email > 4 charac',category='error')
        elif len(username)<2:
            flash('_> Username > 4 charac',category='error')
        elif password1!=password2:
            flash('_> password1!=password2',category='error') 
        elif len(password1)<2:
            flash('_> password > 5 charac',category='error')
        else:
            new_user=User(email=email,username=username,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('User: "'+username+'" Created',category='success')
            ##login_user(user,remember=True)
            ## userResult=db.session.query(User)
            return redirect(url_for("home"))
    return render_template("signup.html") 

if __name__ == '__main__':
    app.run(debug=True)