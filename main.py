from flask import Flask, request, escape, jsonify
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from integer import Integer
from marshmallow_enum import EnumField
from marshmallow import ValidationError, INCLUDE
from models import Session, Tutor, Student, Course, students_in_course, Request, RequestStatus
from schemas import TutorSchema, CourseSchema, StudentSchema, RequestSchema


app = Flask(__name__)
bcrypt = Bcrypt(app)
session = Session()


@app.route('/api/v1/hello-world-27')
def index():
    return 'Hello world 27'


###### works
@app.route('/tutor/<tutor_id>')
def show_tutor(tutor_id):
    schema = TutorSchema()
    tutor = session.query(Tutor).filter(Tutor.id == tutor_id).one_or_none()
    try:
        schema.dump(tutor)
    except ValidationError as err:
        return 'invalid id', 400

    if tutor is None:
        return 'The tutor doesn`t exist', 404
    tutor_schema = TutorSchema(exclude=['password'])
    tutor_res = tutor_schema.dump(tutor)
    return jsonify({'tutor' : tutor_res})

######### works
@app.route('/student/<student_id>')
def show_student(student_id):
    schema = StudentSchema()
    student = session.query(Student).filter(Student.id == student_id).one_or_none()
    try:
        schema.dump(student)
    except ValidationError as err:
        return 'Invalid id', 400

    if student is None:
        return 'The student doesn`t exist', 404

    student_schema = StudentSchema(exclude=['password'])
    student_res = student_schema.dump(student)
    return jsonify({'student' : student_res})


####### works
@app.route('/tutor', methods=['POST'])
def create_tutor():
    tutor_data = request.json
    tutor_schema = TutorSchema()
    parsed = {
        'id': tutor_data['id'],
        'name': tutor_data['name'],
        'surname' : tutor_data['surname'],
        'email' : tutor_data['email'],
        'password': bcrypt.generate_password_hash(tutor_data['password']).decode('utf-8'),
        'age' : tutor_data['age']
    }

    if not session.query(Tutor).filter(Tutor.name == parsed['email']).one_or_none() is None:
        return 'This user already exists', 400
    try:
        tutor = tutor_schema.load(parsed)
    except ValidationError as err:
        return "Invalid data", 400

    session.add(tutor)
    session.commit()
    return 'Token is given. Tutor is registred.'

###### works
@app.route('/tutor/<tutor_id>', methods=['DELETE'])
def delete_tutor(tutor_id):
    tutor = session.query(Tutor).filter(Tutor.id == tutor_id).one_or_none()
    if tutor is None:
        return 'The tutor doesn`t exist', 400
    session.delete(tutor)
    session.commit()
    return 'The tutor is deleted'


####### works
@app.route('/student', methods=['POST'])
def create_student():
    student_data = request.json
    student_schema = StudentSchema()
    parsed = {
        'id': student_data['id'],
        'name': student_data['name'],
        'surname' : student_data['surname'],
        'email' : student_data['email'],
        'password': bcrypt.generate_password_hash(student_data['password']).decode('utf-8'),
        'age' : student_data['age']
    }

    if not session.query(Student).filter(Student.name == parsed['email']).one_or_none() is None:
        return 'This student already exists', 400
    try:
        student = student_schema.load(parsed)
    except ValidationError as err:
        return "Invalid data", 400

    session.add(student)
    session.commit()
    return 'Token is given. Student is registred'


###### works
@app.route('/student/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = session.query(Student).filter(Student.id == student_id).one_or_none()
    if student is None:
        return 'The student doesn`t exist', 400
    session.delete(student)
    session.commit()
    return 'The student is deleted'


####### works
@app.route('/tutor/<tutor_id>/courses')
def show_tutor_courses(tutor_id):
    tutor = session.query(Tutor).filter(Tutor.id == tutor_id).one_or_none()

    if tutor is None:
        return 'The tutor doesn`t exist', 400

    courses = session.query(Course).filter(Course.tutor_id == tutor_id)

    if courses:
        return jsonify(CourseSchema(many=True, exclude=['tutor_id']).dump(courses))
    else:
        return 'There is no courses'


@app.route('/student/<st_id>/my_courses')
def show_students_courses(st_id):
    student = session.query(Student).filter(Student.id == st_id).one_or_none()

    if student is None:
        return 'The student doesn`t exist', 400

    my_courses =  session.query(Course).filter(Course.students.any( Student.id == st_id ))

    if my_courses:
        return jsonify(CourseSchema(many=True).dump(my_courses))
    else:
        return 'There is no courses'


##### works
@app.route('/tutor/<tutor_id>/add', methods=['POST'])
def create_course(tutor_id):
    course_data = request.json
    course_schema = CourseSchema()

    tutor_schema = TutorSchema()
    tutor = session.query(Tutor).filter(Tutor.id == tutor_id).one_or_none()
    try:
        tutor_schema.dump(tutor)
    except ValidationError as err:
        return 'invalid id', 400
    if tutor is None:
        return 'The tutor doesn`t exist', 404

    tutor_schema = TutorSchema(exclude=['password'])
    tutor_res = tutor_schema.dump(tutor)

    parsed = {
        'id' : course_data['id'],
        'student_number' : '0',
        'name': course_data['name'],
        'tutor_id' : tutor_id,
        "students" : [],
    }

    try:
        course = course_schema.load(parsed)
    except ValidationError as err:
        return err.messages, 400

    session.add(course)
    session.commit()
    return "Course is created"


#### works
@app.route('/tutor/<tutor_id>/update', methods=['PUT'])
def update_course(tutor_id):
    tutor_schema = TutorSchema()
    tutor = session.query(Tutor).filter(Tutor.id == tutor_id).one_or_none()
    try:
        tutor_schema.dump(tutor)
    except ValidationError as err:
        return 'invalid id', 400
    if tutor is None:
        return 'The tutor doesn`t exist', 404


    course_data = request.json
    course_schema = CourseSchema()
    course = session.query(Course).filter(Course.id == course_data['id']).one_or_none()

    if course is None:
        return 'The course doesn`t exist', 404

    parsed = {
        'id': course_data['id'],
        'name': course_data['name'],
        'tutor_id': course_data['tutor_id'],
    }

    try:
        data = course_schema.load(parsed)
    except ValidationError as err:
        return err.messages, 400
    course.id = data.id
    course.name = data.name
    course.tutor_id = data.tutor_id
    session.commit()
    return course_schema.dump(course)


##### works
@app.route('/tutor/<tutor_id>/delete/<course_id>', methods=['DELETE'])
def delete_course(tutor_id, course_id):
    tutor_schema = TutorSchema()
    tutor = session.query(Tutor).filter(Tutor.id == tutor_id).one_or_none()
    try:
        tutor_schema.dump(tutor)
    except ValidationError as err:
        return 'invalid id', 400
    if tutor is None:
        return 'The tutor doesn`t exist', 404

    course = session.query(Course).filter(Course.id == course_id).one_or_none()
    if course is None:
        return 'The course doesn`t exist', 400
    session.delete(course)
    session.commit()
    return 'The course is deleted'


#### works
@app.route('/student/<student_id>/request/<course_id>', methods=['POST'])
def create_request(student_id, course_id):

    student = session.query(Student).filter(Student.id == student_id).one_or_none()
    if student is None:
        return 'The student doesn`t exist', 400

    course = session.query(Course).filter(Course.id == course_id).one_or_none()
    if course is None:
        return 'The course doesn`t exist', 400

    if course.student_number > 5:
        return 'You can not join this course', 500

    request_schema = RequestSchema()

    temp_id = Integer(str(student_id)+str(course_id))

    data = {
        'id': temp_id,
        'status': 'placed',
        'student_id' : student_id,
        'course_id' : course_id,
    }

    if not session.query(Request).filter(Request.id == temp_id).one_or_none() is None:
        return 'This request has been sent earlier. Wait for approving', 400
    try:
        request = request_schema.load(data)
    except ValidationError as err:
        return err.messages, 400

    session.add(request)
    session.commit()
    return 'Request has been sent'


### works
@app.route('/tutor/<tutor_id>/request/<request_id>', methods=['PUT'])
def disapprove_request(tutor_id, request_id):
    tutor = session.query(Tutor).filter(Tutor.id == tutor_id).one_or_none()
    if tutor is None:
        return 'The tutor doesn`t exist', 400

    students_request = session.query(Request).filter(Request.id == request_id).one_or_none()
    if students_request is None:
        return 'The request doesn`t exist', 400

    parsed_status = request.json;

    students_request.status = parsed_status['status'] if 'status' in parsed_status else students_request.status

    student = session.query(Student).filter(Student.id == students_request.student_id).one_or_none()

    if parsed_status['status'] == 'approved':
        course = session.query(Course).filter(Course.id == students_request.course_id).one_or_none()
        course.student_number = course.student_number + 1
        course.students.append(student)

    session.commit()
    return 'Request is considered'


if __name__ == '__main__':
    app.run()


# curl -X POST -v -H "Content-Type: application/json" -d '{"field1": "data1", "field2": "data2"}' http://localhost:5000/postendpoint



# @app.route('/api/v1/hello-world-27')
# def hello():
#     name = request.args.get("name", "World 27")
#     return f'Hello {escape(name)}'
#
#
# server = make_server('', 8000, app)
# print('http://127.0.0.1:8000/api/v1/hello-world-27')
# server.serve_forever()
