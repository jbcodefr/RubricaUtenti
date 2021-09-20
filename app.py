from flask import Flask
from flask_restful import reqparse,abort,Api,Resource
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
api=Api(app)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres@localhost/utenti'

db=SQLAlchemy(app)
migrate=Migrate(app,db)

class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(150),unique=True)
    username=db.Column(db.String(150))

def __init__(self,email,username):
    self.email=email
    self.username=username
    
USERS={
    '1':{'email':'foo@bar.com','username':'jean'},
    '2':{'email':'jb@bj.com','username':'jhon'}
}

def abort_if_not_id(userid):
    if userid not in USERS:
        abort('404' ,message="User {} not found".format(userid))
parser=reqparse.RequestParser()
parser.add_argument('userid',type=int,help='User ID')               
parser.add_argument('username',required=True)        
parser.add_argument('email',required=True)        


class User(Resource):
    def get(self,userid):
        abort_if_not_id(userid)
        return USERS[userid]
    
    def delete(self,userid):
        abort_if_not_id(userid)
        del USERS[userid]
        return '',204
    
    def put(self,userid):
        args=parser.parse_args()
        USERS[userid]={'username':args['username'],"email":args['email']}
        return USERS[userid],201
    
class userlist(Resource):
    def get(self):
        return USERS
    def post(self):
        args=parser.parse_args()
        userid=int(max(USERS.keys()).lstrip('userid'))+1
        userid='userid%i'% userid
        USERS[userid]={'username':args['username'],'email':args['email']}
        return USERS[userid],201
    
api.add_resource(User,'/user/<userid>')            
api.add_resource(userlist,'/users')
if __name__ == '__main__':
    app.run(debug=True)