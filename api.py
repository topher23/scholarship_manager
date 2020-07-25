import sqlite3
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from database import Database
from scholarship import *

app = FastAPI()
db = Database()


@app.get('/create_tables')
def create_tables():
    return db.create_tables()

@app.post('/insert_scholarship')
def insert(s : Scholarship):
    result = s.sanitize_insert()
    if result is None:
        return db.insert_into_table(s.create_db_scholarship())
    else:
        return result

@app.get('/fetch_first')
def fetch_first():
    return db.fetch_first()

@app.get('/fetch_all')
def fetch_all():
    return db.fetch_all()

@app.post('/fetch_specific')
def fetch_specific(s : ScholarshipFilter):

    return db.fetch_specific(s)



