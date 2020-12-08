from sqlalchemy.orm import backref
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
import enum
engine = create_engine("postgresql://postgres:123456@localhost:5433/postgres")

SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
Base = declarative_base()



class RequestStatus(enum.Enum):
    placed = "sent"
    approved = "approve"
    delivered = "disapprove"

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    age = Column(String)


students_in_course = Table("students_in_course",
                       Base.metadata,
                       Column("student_id", Integer(), ForeignKey("student.id")),
                       Column("course_id", Integer(), ForeignKey("course.id")))


class Tutor(Base):
    __tablename__ = "tutor"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    age = Column(String)


class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tutor_id = Column(Integer, ForeignKey(Tutor.id))
    tutor = relationship(Tutor, backref="course", lazy=False)
    students = relationship(Student, secondary=students_in_course, lazy="subquery",
                            backref=backref("course", lazy=True))

class Request(Base):
    __tablename__ = "request"
    id = Column(Integer, primary_key=True)
    status = Column(Enum(RequestStatus))
    student_id = Column(Integer, ForeignKey(Student.id))
    student = relationship(Student, backref="request", lazy=False)
    course_id = Column(Integer, ForeignKey(Course.id))
    course = relationship(Course, backref="request", lazy=False)

Base.metadata.create_all(engine)