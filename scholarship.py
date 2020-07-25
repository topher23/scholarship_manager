import random as rand
from datetime import datetime, date
from typing import Optional, Any

from pydantic.main import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from base_scholarship import BaseScholarship
from returns import Returns

Base = declarative_base()


class ScholarshipDB(Base):
    __tablename__ = 'scholarships'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    desc = Column(String)
    requirements = Column(String)
    source = Column(String)
    deadline = Column(String)
    amount = Column(Integer)
    school = Column(String)
    major = Column(String)
    handedness = Column(String)
    extracurricular = Column(String)
    gender = Column(String)
    location = Column(String)

    def clean_as_dict(self):
        d = {}
        for column in self.__table__.columns:
            if str(getattr(self, column.name)) != "[None]" and str(getattr(self, column.name)) != "None" and column.name != "id":
                d[column.name] = str(getattr(self, column.name))

        return d


class Scholarship(BaseScholarship):
    amount: int

    def sanitize_insert(self):
        if all(v is None for v in [self.title, self.desc, self.requirements, self.source, self.deadline, self.amount]):
            return Returns(False, "one more more required variables is null. Required variables are title, desc, "
                                  "requirements, source, deadline, and amount.").response()
        return_val = None
        if self.handedness is not None:
            return_val = self.sanitize_handedness()
        if return_val is None and self.merit_or_need_based is not None:
            return_val = self.sanitize_merit_or_need_based()
        if return_val is None and self.gender is not None:
            return_val = self.sanitize_gender()
        return return_val

    def create_db_scholarship(self):
        return ScholarshipDB( title=self.title, desc=self.desc, requirements=self.requirements,
                             source=self.source, deadline=str(self.deadline), amount=self.amount, school=str(self.school),
                             major=self.major, handedness=self.handedness, extracurricular=str(self.extracurricular),
                             gender=self.gender, location=str(self.location))

class ScholarshipFilter(BaseScholarship):
    amount_greater_than: Optional[int]
    amount_less_than: Optional[int]

    def sanitize_fetch(self):
        return_val = self.sanitize_handedness()
        if return_val is None:
            return_val = self.sanitize_merit_or_need_based()
        if return_val is None:
            return_val = self.sanitize_gender()
        if return_val is None:
            return_val = self.sanitize_school()
        if return_val is None:
            return_val = self.sanitize_extracurricular()
        if return_val is None:
            return_val = self.sanitize_location()
        if return_val is None:
            return_val = self.sanitize_extracurricular()
        return return_val