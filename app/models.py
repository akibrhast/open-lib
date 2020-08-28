
from app import db

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
    
        return f"<id: {self.id},name: {self.title},key: {self.object_key},author: {self.author}>"


