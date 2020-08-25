from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
import os
from flask_sqlalchemy import SQLAlchemy


#from flask_login import login_user, current_user, logout_user, login_required #Optional login imports, need to 'pip install flask_login'


# import boto3
# from botocore.client import Config

# # Get the service client with sigv4 configured
# s3 = boto3.client('s3', config=Config(signature_version='s3v4') ,    aws_access_key_id="AKIAJTRZTPK26SP27X6Q",
#     aws_secret_access_key="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")

# # Generate the URL to get 'key-name' from 'bucket-name'
# # URL expires in 604800 seconds (seven days)
# url = s3.generate_presigned_url(
#     ClientMethod='get_object',
#     Params={
#         'Bucket': 'books202',
#         'Key': 'Books-20200623T203822Z-002/Books/Artemis Fowl/01 artemis fowl - eoin colfer.pdf'
#     },
#     ExpiresIn=604800
# )






app = Flask(__name__)
#postgres://rccubcqkcflzgf:9586b06abbbb73023074a4be39063f07daa68fc3ca77f054941712737ed9809d@ec2-52-87-58-157.compute-1.amazonaws.com:5432/df76b2kmkiedk3
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://rccubcqkcflzgf:9586b06abbbb73023074a4be39063f07daa68fc3ca77f054941712737ed9809d@ec2-52-87-58-157.compute-1.amazonaws.com:5432/df76b2kmkiedk3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


books = [{"name" : "Artemis Fowl Book 1",
        "url" : "https://books2020.s3.amazonaws.com/Books-20200623T203822Z-002/Books/Artemis+Fowl/01+artemis+fowl+-+eoin+colfer.pdf"},
        {"name" : "Artemis Fowl Book 2",
        "url" : "https://books2020.s3.amazonaws.com/Books-20200623T203822Z-002/Books/Artemis+Fowl/02+the+arctic+incident+-+eoin+colfer.pdf"},
        {"name" : "Artemis Fowl Book 3",
        "url" : "https://books2020.s3.amazonaws.com/Books-20200623T203822Z-002/Books/Artemis+Fowl/04+the+opal+deception+-+eoin+colfer.pdf"}
        
        ]
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
    return render_template("simpleviewer.html",awsUrl = awsUrl)
    
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0',debug=True)
