from app import app
from db import db

db.init_app(app)


# It's done to avoid db mistake.
@app.before_first_request
def create_tables():
    db.create_all()
