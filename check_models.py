from lab_flask_1.models import *

# psql -h localhost -d postgres -U postgres -p 5433 -a -q -f create_table.sql

session = Session()

student = Student(id=1, name='Alina', surname='Dziamba', email='jhgf',age ='18')
tutor1 = Tutor(id=3, name='A', surname='D', email='viktoriahall14@gmail.com', password = "qwerty", age ='28')
student6 = Student(id=12, name='Khrystyna', surname='P', email='jgf', password = "qwerty", age ='8')
student7 = Student(id=53, name='Alin', surname='Dziamb', email='jgf', password = "qwerty", age ='8')
student8 = Student(id=9, name='Alin', surname='Dziamb', email='jgf', password = "qwerty",age ='8')
course = Course(id=15, name='Al', student_number = 2,  tutor_id=3, students = [student6, student7])
course1 = Course(id=40, name='Al', student_number = 2, tutor_id=3, students = [student6, student7])
# request = Request(id =0 , status = RequestStatus.placed, student_id = student6.id, course_id=course.id)

session.add(student)
session.add(tutor1)
session.add(student6)
session.add(student7)
session.add(student8)
session.add(course)
session.add(course1)
# session.add(request)
session.commit()
