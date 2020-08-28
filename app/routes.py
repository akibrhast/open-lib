from app import app, db
from app.models import Books
from app import Config


from flask import  flash, redirect, render_template, request, session, abort,url_for
import os
import itertools 
import boto3



@app.route('/')
def index():
    #books = Books.query.all()
    books = Books.query.order_by(Books.author).all()
    authors = sorted(set(book.author for book in books))
    return render_template("home.html",books=books,authors=authors)


@app.route("/read/<book_id>")
def read(book_id):
    book = Books.query.get(book_id)
    s3Client = boto3.client('s3',
                            aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
                            aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])
    url = s3Client.generate_presigned_url(ClientMethod='get_object',
                                            Params={'Bucket': 'books2020', 'Key': book.object_key},
                                            ExpiresIn=600)
    return render_template("mobile-viewer.html",awsUrl = url)

@app.route("/save_page", methods=['POST'])
def save_page():

    print(request.data)
    return {"status":"Successfully Saved"}

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0',debug=True)