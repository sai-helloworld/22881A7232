from . import db
from datetime import datetime, timedelta

class ShortURL(db.Model):
    __tablename__ = 'short_urls'

    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    valid_time = db.Column(db.Integer, default=30)  # validity in minutes
    clicks = db.Column(db.Integer, default=0)

    def is_valid(self):
        return datetime.utcnow() < self.created_at + timedelta(minutes=self.valid_time)
