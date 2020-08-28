from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import itertools 


import boto3

# books=[]
# s3 = boto3.resource('s3',aws_access_key_id="AKIAJTRZTPK26SP27X6Q", aws_secret_access_key="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")
s3Client = boto3.client('s3',aws_access_key_id="AKIAJTRZTPK26SP27X6Q",aws_secret_access_key="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")

# my_bucket = s3.Bucket('books2020')

# for my_bucket_object in my_bucket.objects.all():
#     if ".pdf" in my_bucket_object.key:
#         url = s3Client.generate_presigned_url(ClientMethod='get_object',Params={'Bucket': 'books2020', 'Key': my_bucket_object.key  }, ExpiresIn=604800)
#         books.append({"name":my_bucket_object.key,"url":url})

app = Flask(__name__)
#postgres://rccubcqkcflzgf:9586b06abbbb73023074a4be39063f07daa68fc3ca77f054941712737ed9809d@ec2-52-87-58-157.compute-1.amazonaws.com:5432/df76b2kmkiedk3
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://rccubcqkcflzgf:9586b06abbbb73023074a4be39063f07daa68fc3ca77f054941712737ed9809d@ec2-52-87-58-157.compute-1.amazonaws.com:5432/df76b2kmkiedk3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)





#id | title | series | series_position | author | img_url | object_key | e_tag
class Books(db.Model):
    __tablename__ = 'books'

    id              = db.Column(db.Integer, primary_key=True)
    title            = db.Column(db.String())
    series          = db.Column(db.String())
    series_position = db.Column(db.Integer())
    author          = db.Column(db.String())
    img_url         = db.Column(db.String())
    object_key      = db.Column(db.String())
    e_tag           = db.Column(db.String())


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





@app.route('/')
def index():
    #books = Books.query.all()
    books = Books.query.order_by(Books.author).all()
    authors = set(book.author for book in books)
    return render_template("home.html",books=books,authors=authors)


@app.route("/read/<book_id>")
def read(book_id):
    book = Books.query.get(book_id)
    url = s3Client.generate_presigned_url(ClientMethod='get_object',
                                            Params={'Bucket': 'books2020', 'Key': book.object_key  },
                                            ExpiresIn=600)
    return render_template("mobile-viewer.html",awsUrl = url)
    
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0',debug=True)
