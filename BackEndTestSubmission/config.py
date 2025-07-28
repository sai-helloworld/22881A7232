import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:pass123@localhost:3306/url_shortener'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
