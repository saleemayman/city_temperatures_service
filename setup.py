from app import app
from models import db

with app.app_context():
    # create the DB
    db.create_all()