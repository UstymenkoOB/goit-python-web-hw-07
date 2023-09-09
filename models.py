from datetime import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship

from connect_db import engine

Base = declarative_base()

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)    
    teacher_id = Column(Integer, ForeignKey(Teacher.id, ondelete="CASCADE"))
    teacher = relationship(Teacher, backref="subjects")
    
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)    
    group_id = Column(Integer, ForeignKey(Group.id, ondelete="CASCADE", onupdate="CASCADE"))   
    group = relationship(Group, backref="students")  
    
class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    grade_date = Column(DateTime, default=datetime.now())
    grade = Column(Integer)
    student_id = Column(Integer, ForeignKey(Student.id, ondelete="CASCADE", onupdate="CASCADE"))
    student = relationship(Student, backref="grades") 
    teacher_id = Column(Integer, ForeignKey(Teacher.id, ondelete="CASCADE", onupdate="CASCADE"))
    teacher = relationship(Teacher, backref="grades")
    subject_id = Column(Integer, ForeignKey(Subject.id, ondelete="CASCADE", onupdate="CASCADE"))
    subject = relationship(Subject, backref="grades") 

Base.metadata.create_all(engine)
Base.metadata.bind = engine