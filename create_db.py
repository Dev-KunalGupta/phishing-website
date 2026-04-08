from app import app
from database import db

from models.db_models import ScanHistory, ReportedURL

with app.app_context():
    db.create_all()
    print("Database created successfully!")