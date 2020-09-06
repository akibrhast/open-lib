  
from app import app, db
from app.models import Books,User,Reading


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Books': Books,"Reading":Reading,"User":User}