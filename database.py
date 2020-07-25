
from sqlalchemy import create_engine, exc, or_, any_
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from returns import Returns
from scholarship import *
from sqlalchemy.orm import sessionmaker


class Database():
    def __init__(self):
        self.engine = create_engine('sqlite:///scholarship.db', echo=True)

    def create_tables(self):
        try:
            Base.metadata.create_all(self.engine)
        except exc.SQLAlchemyError as e:
            print(e)
            return Returns(False, "failed to build tables. Error: " + str(e)).response()
        return Returns(True, "successfully built tables or they already existed").response()

    def insert_into_table(self, s_db):
        try:
            session = sessionmaker(bind=self.engine)()
            session.add(s_db)
            session.commit()
        except exc.SQLAlchemyError as e:
            print(e)
            return Returns(False, "failed to insert into table. Error: " + str(e)).response()
        return Returns(True, "successfully inserted into table. Payload: " + str(s_db)).response()

    def fetch_first(self):
        try:
            session = sessionmaker(bind=self.engine)()
            scholarship = session.query(ScholarshipDB).first()
        except exc.SQLAlchemyError as e:
            print(e)
            return Returns(False, "failed to fetch from db. Error: " + str(e)).response()
        return Returns(True, scholarship).response()

    def fetch_all(self):
        try:
            session = sessionmaker(bind=self.engine)()
            scholarship = session.query(ScholarshipDB).all()
        except exc.SQLAlchemyError as e:
            print(e)
            return Returns(False, "failed to fetch from db. Error: " + str(e)).response()
        return Returns(True, scholarship).response()

    def fetch_specific(self, s):
        session = sessionmaker(bind=self.engine)()
        q = session.query(ScholarshipDB)
        if s.title is not None:
            q = q.filter(ScholarshipDB.title == s.title)
        if s.desc is not None:
            q = q.filter(ScholarshipDB.desc == s.desc)
        if s.requirements is not None:
            q = q.filter(ScholarshipDB.requirements == s.requirements)
        if s.source is not None:
            q = q.filter(ScholarshipDB.source == s.source)
        if s.deadline is not None:
            q = q.filter(ScholarshipDB.deadline == s.deadline)
        if s.major is not None:
            q = q.filter(ScholarshipDB.major == s.major)
        if s.handedness is not None:
            q = q.filter(ScholarshipDB.handedness == s.handedness)
        if s.gender is not None:
            q = q.filter(ScholarshipDB.gender == s.gender)
        if s.amount_greater_than is not None:
            q = q.filter(s.amount_greater_than <= ScholarshipDB.amount)
        if s.amount_less_than is not None:
            q = q.filter(s.amount_less_than >= ScholarshipDB.amount)
        if s.school is not None:
            q = q.filter(or_(*[ScholarshipDB.school.contains(x) for x in s.school]))
        if s.location is not None:
            q = q.filter(or_(*[ScholarshipDB.location.contains(x) for x in s.location]))
        if s.extracurricular is not None:
            q = q.filter(or_(*[ScholarshipDB.extracurricular.contains(x) for x in s.extracurricular]))
        return q.all()
