from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
import os
from flask_sqlalchemy import SQLAlchemy
# import boto3

# #from flask_login import login_user, current_user, logout_user, login_required #Optional login imports, need to 'pip install flask_login'





# # Get the service client with sigv4 configured
# s3 = boto3.client('s3',    aws_access_key_id="AKIAJTRZTPK26SP27X6Q",aws_secret_access_key="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")

# # Generate the URL to get 'key-name' from 'bucket-name'
# # URL expires in 604800 seconds (seven days)

# url = s3.generate_presigned_url(ClientMethod='get_object',Params={'Bucket': 'books2020', 'Key': 'Books-20200623T203822Z-002/Books/BrandonSanderson.works/The Stormlight Archieve/Words of Radiance by Brandon Sanderson/words of radiance by brandon sanderson.pdf'  }, ExpiresIn=604800)



import boto3

books=[]
s3 = boto3.resource('s3',aws_access_key_id="AKIAJTRZTPK26SP27X6Q", aws_secret_access_key="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")
s3Client = boto3.client('s3',aws_access_key_id="AKIAJTRZTPK26SP27X6Q",aws_secret_access_key="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")

my_bucket = s3.Bucket('books2020')

for my_bucket_object in my_bucket.objects.all():
    if ".pdf" in my_bucket_object.key:
        url = s3Client.generate_presigned_url(ClientMethod='get_object',Params={'Bucket': 'books2020', 'Key': my_bucket_object.key  }, ExpiresIn=604800)
        books.append({"name":my_bucket_object.key,"url":url})

app = Flask(__name__)
#postgres://rccubcqkcflzgf:9586b06abbbb73023074a4be39063f07daa68fc3ca77f054941712737ed9809d@ec2-52-87-58-157.compute-1.amazonaws.com:5432/df76b2kmkiedk3
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://rccubcqkcflzgf:9586b06abbbb73023074a4be39063f07daa68fc3ca77f054941712737ed9809d@ec2-52-87-58-157.compute-1.amazonaws.com:5432/df76b2kmkiedk3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)



#id | book_name | series_name | author_name

'''
Display book by Series Name:
Artemis Fowl
    ->artermis fowl book 1
    ->artermis fowl book 2
    ->artermis fowl book 3
Mistborn
    ->mistborn book1
    ->mistborn book2
    ->mistborn book3
Words 
'''

class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    pdf_file = db.Column(db.LargeBinary())

    def __init__(self, name, pdf_file):
        self.name = name
        self.pdf_file = pdf_file


    def __repr__(self):
    
        return f"<Book {self.name}>"

@app.route('/')
def index():


    
    return render_template("home.html",books=books)


@app.route("/read/<book_url>")
def read(book_url):
    awsUrl = books[int(book_url)]["url"]
    print(awsUrl)
    return render_template("mobile-viewer.html",awsUrl = awsUrl)
    
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0',debug=True)
