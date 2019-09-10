from toolbox import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

#loads current user
@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


#Create users table


class User(db.model,UserMixin):

    __tablename__='users'

    id = db.Column(db.Integer,primary_key = True)

    email = db.Column(db.String(64),unique = True, index=True)

    username = db.Column(db.String(64),unique = True, index=True)

    password_hash = db.Column(db.String(128))


 #Representation of the users
    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

#Check password with hash password
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
