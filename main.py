from random import randint
from sqlalchemy import and_, desc, func, select

from connect_db import session
from constants import NUMBER_GROUPS, NUMBER_STUDENTS, NUMBER_SUBJECTS, NUMBER_TEACHERS
from models import Student, Subject, Teacher, Group, Grade

def queries(n):
    match n:
      case 1:
          q = session.query(Student.name, 
                            func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
          .select_from(Grade).join(Student).group_by(Student.id)\
          .order_by(desc('avg_grade')).limit(5).all()
      case 2:
          subject_id = randint(1, NUMBER_SUBJECTS)
          q = session.query(Subject.name, Student.name,
                            func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
          .select_from(Grade).join(Student).join(Subject).filter(Subject.id == subject_id)\
          .group_by(Subject.id, Student.id).order_by(desc('avg_grade')).limit(1).all()
      case 3:
          subject_id = randint(1, NUMBER_SUBJECTS)
          q = session.query(Subject.name, 
                            Group.name,
                            func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
          .select_from(Grade).join(Student).join(Subject).join(Group).filter(Subject.id == subject_id)\
          .group_by(Subject.id, Group.id).all()      
      case 4:
          q = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')).all()
      case 5:
          teacher_id = randint(1, NUMBER_TEACHERS)
          q = session.query(Teacher.name, 
                            Subject.name)\
          .select_from(Subject).join(Teacher).filter(Teacher.id == teacher_id).all()
      case 6:
          group_id = randint(1, NUMBER_GROUPS)
          q = session.query(Group.name, 
                            Student.name)\
          .select_from(Student).join(Group).filter(Group.id == group_id)\
          .order_by(Student.name).all()
      case 7:
          group_id = randint(1, NUMBER_GROUPS)
          subject_id = randint(1, NUMBER_SUBJECTS)
          q = session.query(Group.name, 
                            Subject.name, 
                            Student.name, 
                            Grade.grade)\
          .join(Student, Student.group_id == Group.id)\
          .join(Grade, Student.id == Grade.student_id)\
          .join(Subject, Grade.subject_id == Subject.id)\
          .filter(Student.id.in_(session.query(Student.id).filter(Student.group_id == group_id)))\
          .filter(Grade.subject_id == subject_id)\
          .order_by(Student.name).all()
      case 8:
          teacher_id = randint(1, NUMBER_TEACHERS)
          q = session.query(Teacher.name,
                            func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
          .join(Grade, Teacher.id == Grade.teacher_id)\
          .filter(Grade.teacher_id == teacher_id)\
          .group_by(Teacher.id).all()
      case 9:
          student_id = randint(1, NUMBER_STUDENTS)
          q = session.query(
              Student.name,
              Subject.name)\
          .join(Grade, Student.id == Grade.student_id)\
          .join(Subject, Grade.subject_id == Subject.id)\
          .filter(Grade.student_id == student_id)\
          .group_by(Student.id, Subject.name)\
          .order_by(Subject.name).all()
      case 10:
          teacher_id = randint(1, NUMBER_TEACHERS)
          student_id = randint(1, NUMBER_STUDENTS)
          q = session.query(
              Student.name,
              Teacher.name,
              Subject.name)\
          .join(Grade, Grade.student_id == Student.id,)\
          .join(Subject, Grade.subject_id == Subject.id)\
          .join(Teacher, Grade.teacher_id == Teacher.id)\
          .filter(and_(Grade.student_id == student_id, Grade.teacher_id == teacher_id))\
          .group_by(Student.name, Teacher.name, Subject.name).all()
      case 11:
          teacher_id = randint(1, NUMBER_TEACHERS)
          student_id = randint(1, NUMBER_STUDENTS)
          q = session.query(Student.name,
                            Teacher.name,
                            func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
          .join(Student, Grade.student_id == Student.id)\
          .join(Teacher, Grade.teacher_id == Teacher.id)\
          .filter(and_(Grade.student_id == student_id, Grade.teacher_id == teacher_id))\
          .group_by(Student.name, Teacher.name).all()
      case 12:
          group_id = randint(1, NUMBER_GROUPS)
          subject_id = randint(1, NUMBER_SUBJECTS)

          subquery = session.query(func.max(Grade.grade_date)).filter(
              Grade.student_id.in_(
                  session.query(Student.id).filter(Student.group_id == group_id)
              ),
              Grade.subject_id == subject_id
          ).scalar_subquery()

          q = session.query(
              Grade.grade_date,
              Group.name,
              Subject.name,
              Student.name,
              Grade.grade
          ).join(Student, Grade.student_id == Student.id)\
          .join(Subject, Grade.subject_id == Subject.id)\
          .join(Group, Student.group_id == Group.id)\
          .filter(
              Grade.student_id.in_(
                  session.query(Student.id).filter(Student.group_id == group_id)
              ),
              Grade.subject_id == subject_id,
              Grade.grade_date == subquery
          ).all()
      case _:
          q = "No such query"
    return q

if __name__ == '__main__':
    print(queries(12))
   