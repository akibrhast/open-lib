from app import app, db
from app.models import Books
from app import Config
import pandas as pd


from flask import  flash, redirect, render_template, request, session, abort,url_for
import os
import itertools 
import boto3

s3Client = boto3.client('s3',
                        aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])

def create_template_ready_dict(df):
    d={}
    for i in set(df.author):
        d[i]={}
        df2=df[df.author==i]
        for k in set(df2.series):
            d[i][k]=[]
            df3=df2[df2.series==k]
            for j in range(len(df3)):
                d[i][k].append({'title':df3['title'].iloc[j], 
                                'series_position':df3['series_position'].iloc[j],
                                'page_number':df3['page_number'].iloc[j],
                                'id':df3['id'].iloc[j],
                                'object_key':df3['object_key'].iloc[j]
                                })
    for key0,value0 in d.items():
        for key1,value1 in value0.items():       
            value1 = sorted(value1, key = lambda i: i['series_position'])
            d[key0][key1] = value1
    return d


@app.route('/')
def index():
    df = pd.read_sql("""SELECT 
                            id,author,series,series_position,title,page_number,object_key 
                        FROM 
                            books
                    """, db.session.bind)
    d = create_template_ready_dict(df)

    return render_template("home.html",mydf=d)


@app.route("/read")
def read():
    url = s3Client.generate_presigned_url(ClientMethod='get_object',
                                          Params={'Bucket': 'books2020', 'Key': request.args.get('object_key')},
                                          ExpiresIn=600)
    
    return render_template("web/viewer.html",
                            awsUrl=url,
                            pageNumber = request.args.get('getpage_number'),
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