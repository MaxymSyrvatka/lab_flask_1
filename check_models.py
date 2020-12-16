from models import *

# psql -h localhost -d postgres -U postgres -p 5433 -a -q -f create_table.sql

session = Session()

tutor1 = Tutor(id=0, name='Ann', surname='Di', email='ann@',age=28)
student1 = Student(id=0, name='Alin', surname='Dziamb', email='alin@',age=18)
student2 = Student(id=1, name='Khrist', surname='Dziamb', email='kh@',age=21)
student3 = Student(id=2, name='Ann', surname='Dziamb', email='AV@',age=20)
course = Course(id=0, name='math', tutor=tutor1, students=[student1, student2])
course1 = Course(id=1, name='history', tutor=tutor1, students=[student3, student2])
request = Request(id=0, status=RequestStatus.placed, student=student1, course=course)
request1 = Request(id=1, status=RequestStatus.placed, student=student3, course=course)


session.add(tutor1)
session.add(student1)
session.add(student2)
session.add(student3)
session.add(course)
session.add(course1)
session.add(request)
session.add(request1)
session.commit()
