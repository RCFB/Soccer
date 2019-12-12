from flask_login import UserMixin, LoginManager, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import app
from .database import db, fetchall

login_manager = LoginManager() # création d'un objet de la classe LoginManager
login_manager.init_app(app)    # association de cet objet à l'application

# Classe associée aux utilisateurs non authentifiés
class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        self.id = None
        self.admin = False

# association de cette classe au manager de connexion
login_manager.anonymous_user = AnonymousUser 

# association de cette classe au manager de connexion
@login_manager.user_loader
def user_loader(user_id):
    return find_user_by_id(user_id)

class User(UserMixin):
    def __init__(self):
        self.email = None
        self.password_hash = None
        self.id = None
        self.admin = False

    def set_id(self, id):
        self.id = id


    def set_email(self, email):
        self.email = email
        

    def set_admin(self, admin):
        self.admin = admin
        

    def set_password_hash(self, password_hash):
        self.password_hash=password_hash
        

    def set_password(self, password):
        hash = generate_password_hash(password)
        self.set_password_hash(hash)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        if self.id is None:
            insert_user(self)
        else:
            update_user(self)


def fill_db():
    admin = User()
    admin.set_email('admin@example.com')
    admin.set_password('admin')
    admin.set_admin(True)
    admin.save()

def insert_user(user):
     cursor = db.cursor()
     cursor.execute('''
        INSERT INTO users(email, password_hash, admin)
        VALUES (:email, :password_hash, :admin)
        ''',{
            'email' : user.email, 
            'password_hash' : user.password_hash,
            'admin' : 1 if user.admin else 0
            })
     user.set_id(cursor.lastrowid)
     db.commit()
     print(vars(user))

def update_user(user):
    print(vars(user))
    cursor = db.cursor()
    cursor.execute('''
     UPDATE users
        SET email = :email,
            password = :password_hash, 
            admin = :admin
            WHERE id = :id
        ''',{
            'id' : user.id,
            'email' : user.email,
            'password_hash' : user.password_hash,
            'admin' : 1 if user.admin else 0
            })
    user.set_id(cursor.lastrowid)
    db.commit()
    print(vars(user))

def user_from_row(row):
    user = User()
    user.set_id(row['id'])
    user.set_email(row['email'])
    user.set_password_hash(row['password_hash'])
    user.set_admin(row['admin'] == 1)
    return user


def find_user_by_email(email):
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM users WHERE email = :email''', {'email' : email})
    result = fetchall(cursor)
    if len(result) == 0:
        return None
    return user_from_row(result[0])

def find_user_by_id(id):
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM users WHERE id = :id''', {'id' : id})
    result = fetchall(cursor)
    if len(result) == 0:
        return None
    return user_from_row(result[0])

def users():
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM users''')
    return fetchall(cursor)