from app import app, db
from app.models import Books, User
from app import Config

from flask_login import current_user, login_user, login_required, logout_user


from flask import  flash, redirect, render_template, request, session, abort,url_for
import os
import itertools 
import boto3
from werkzeug.urls import url_parse
from app.forms import RegistrationForm, LoginForm


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
                                'object_key':j.object_key})
    return n



@app.route('/')
@login_required
def index():
    books = Books.query.order_by(Books.author).all()
    return render_template("home.html",mydf=create_template_ready_dict(books))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
#@login_required
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/read")
@login_required
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

    book = Books.query.filter_by(id=request.get_json()['book_id']).first_or_404()
    book.page_number = int(request.get_json()['page_number'])
    db.session.commit()

    return {"status":"Successfully Saved"}


    
@app.route("/search",methods=['POST'])
def search():
    
    return request.get_json()
    



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0',debug=True)