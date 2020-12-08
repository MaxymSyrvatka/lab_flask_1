from models import *

# psql -h localhost -d postgres -U postgres -p 5433 -a -q -f create_table.sql

session = Session()
##student = Student(id=1, name='Alina', surname='Dziamba', email='jhgf',age ='18')
tutor1 = Tutor(id=3, name='A', surname='D', email='j',age ='28')
student6 = Student(id=6, name='Alin', surname='Dziamb', email='jgf',age ='8')
student7 = Student(id=5, name='Alin', surname='Dziamb', email='jgf',age ='8')
student8 = Student(id=55, name='Alin', surname='Dziamb', email='jgf',age ='8')
course = Course(id=105, name='Al', tutor=tutor1, students = [student6, student7])
course1 = Course(id=40, name='Al', tutor=tutor1, students = [student6, student7])
request = Request(id =550 , status = RequestStatus.placed, student = student6, course=course)

##session.add(student)
session.add(tutor1)
session.add(student6)
session.add(student7)
session.add(student8)
session.add(course)
session.add(course1)
session.add(request)
session.commit()