from app import app, db
from app.models import Books
from app import Config


from flask import  flash, redirect, render_template, request, session, abort,url_for
import os
import itertools 
import boto3

s3Client = boto3.client('s3',
                        aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])

def create_template_ready_dict(books):
    n={}
    for i in set([book.author for book in books]):
        n[i] = {}
        books2= [book for book in books if book.author==i]
        for k in set([book.series for book in books2]):
            n[i][k] = []
            books3 = [book for book in books2 if book.series==k]
            for j in books3:
                n[i][k].append({'title':j.title, 
                                'series_position':j.series_position,
                                'page_number':j.page_number,
                                'id':j.id,
                                'object_key':j.object_key
                                })
    return n


@app.route('/')
def index():
    books = Books.query.order_by(Books.author).all()
    return render_template("home.html",mydf=create_template_ready_dict(books))


@app.route("/read")
def read():
    url = s3Client.generate_presigned_url(ClientMethod='get_object',
                                          Params={'Bucket': 'books2020', 'Key': request.args.get('object_key')},
                                          ExpiresIn=600)
    
    return render_template("web/viewer.html",
                            awsUrl=url,
                            pageNumber = request.args.get('page_number'),
                            bookId=request.args.get('id')
                            )

@app.route("/save_page", methods=['POST'])
def save_page():
    
    book = Books.query.filter_by(id=int(request.get_json()['book_id'])).first_or_404()
    book.page_number = int(request.get_json()['page_number'])
    db.session.commit()

    '''
    result = db.engine.execute(" UPDATE books SET page_number=%s WHERE id=%s",
                                (int(request.get_json()['page_number']),request.get_json()['book_id'],)
                                )
    '''
    return {"status":"Successfully Saved"}




if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0',debug=True)