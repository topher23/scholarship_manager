from datetime import date

from pydantic.main import BaseModel
from typing import Optional, Any

from returns import Returns


class BaseScholarship(BaseModel):

    title: Optional[str]
    desc: Optional[str]
    requirements: Optional[str]
    source: Optional[str]
    deadline: Optional[date]
    merit_or_need_based: Optional[str]
    school: Optional[list]
    major: Optional[str]
    handedness: Optional[str]
    extracurricular: Optional[list]
    gender: Optional[str]
    location: Optional[list]

    def sanitize_merit_or_need_based(self):
        if self.merit_or_need_based.lower() == 'merit':
            self.handedness = 'merit'
        elif self.merit_or_need_based.lower() == 'need':
            self.handedness = 'need'
        elif self.merit_or_need_based.lower() == 'both':
            self.handedness = 'both'
        else:
            return Returns(False, "merit/need based field is wrong. use word 'merit', 'need', or 'both'").response()
        return

    def sanitize_handedness(self):
        if self.handedness.lower() == 'l' or self.handedness.lower() == 'left':
            self.handedness = 'left'
        elif self.handedness.lower() == 'r' or self.handedness.lower() == 'right':
            self.handedness = 'right'
        elif self.handedness.lower() == 'both' or self.handedness.lower() == 'ambidextrous':
            self.handedness = 'both'
        else:
            return Returns(False, "handedness field is wrong. use word 'left', 'right', or 'other'").response()
        return

    def sanitize_gender(self):
        if self.gender.lower() == 'm' or self.gender.lower() == 'male':
            self.gender = 'male'
        elif self.gender.lower() == 'f' or self.gender.lower() == 'female':
            self.gender = 'female'
        elif self.gender.lower() == 'o' or self.gender.lower() == 'other':
            self.gender = 'other'
        elif self.gender.lower() == 'b' or self.gender.lower() == 'both':
            self.gender = 'both'
        else:
            return Returns(False, "gender field is wrong. use word 'male', 'female', 'both', or 'other'").response()
        return