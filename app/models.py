
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

#id | title | series | series_position | author | img_url | object_key | e_tag | page_number
class Books(db.Model):
    __tablename__ = 'books'


    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String())
    series          = db.Column(db.String())
    series_position = db.Column(db.Integer())
    author          = db.Column(db.String())
    img_url         = db.Column(db.String())
    object_key      = db.Column(db.String())
    e_tag           = db.Column(db.String())
    page_number     = db.Column(db.Integer())

    def __init__(self, title, series,series_position,author,img_url,object_key,e_tag):
        self.title  = tile
        self.series = series
        self.series_position = series_position
        self.author = author
        self.img_url = img_url
        self.object_key = object_key
        self.e_tag = e_tag
    

    def __repr__(self):

        
        return f"<id: {self.id},title: {self.title},key: {self.object_key},author: {self.author}>"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.email)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))