from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt, check_password_hash
from flask_httpauth import HTTPBasicAuth
from integer import Integer
from marshmallow import ValidationError, INCLUDE
from models import Session, Tutor, Student, Course, students_in_course, Request, RequestStatus
from schemas import TutorSchema, CourseSchema, StudentSchema, RequestSchema


app = Flask(__name__)
auth = HTTPBasicAuth()
bcrypt = Bcrypt(app)
session = Session()


@app.route('/api/v1/hello-world-27')
def index():
    return 'Hello world 27'


@auth.verify_password
def authenticate(username, password):
    tutor = session.query(Tutor).filter(Tutor.email == username).one_or_none()
    student = session.query(Student).filter(Student.email == username).one_or_none()
    if tutor is not None:
        if username and password:
            if check_password_hash(tutor.password, password):
                return True
            else:
                return False
    if student is not None:
        if username and password:
            if check_password_hash(student.password, password):
                return True
            else:
                return False
    return False


# @app.route('/logout')
# @auth.login_required
# def logout():
#     return "You are logged out!", 401


@app.route('/tutor/<tutor_id>')
@auth.login_required
def show_tutor(tutor_id):
    schema = TutorSchema()
    tutor = session.query(Tutor).filter(Tutor.id == tutor_id).one_or_none()
    try:
        schema.dump(tutor)
    except ValidationError as err:
        return 'invalid id', 400

    if tutor is None:
        return 'The tutor doesn`t exist', 404

    if auth.current_user() != tutor.email:
        return 'You don`t have a permission to see information about this tutor!', 401
    tutor_schema = TutorSchema(exclude=['password'])
    tutor_res = tutor_schema.dump(tutor)
    return jsonify({'tutor': tutor_res})


@app.route('/student/<student_id>')
@auth.login_required
def show_student(student_id):
    schema = StudentSchema()
    student = session.query(Student).filter(Student.id == student_id).one_or_none()
    try:
        schema.dump(student)
    except ValidationError as err:
        return 'Invalid id', 400

    if student is None:
        return 'The student doesn`t exist', 404

    if auth.current_user() != student.email:
        return 'You don`t have a permission to see information about this student!', 401

    student_schema = StudentSchema(exclude=['password'])
    student_res = student_schema.dump(student)
    return jsonify({'student': student_res})


@app.route('/tutor', methods=['POST'])
def create_tutor():
    tutor_data = request.json
    tutor_schema = TutorSchema()
    parsed = {
        'id': tutor_data['id'],
        'name': tutor_data['name'],
        'surname': tutor_data['surname'],
        'email': tutor_data['email'],
        'password': bcrypt.generate_password_hash(tutor_data['password']).decode('utf-8'),
        'age': tutor_data['age']
    }

    if (session.query(Tutor).filter(Tutor.email == parsed['email']).one_or_none() is not None) or \
            (session.query(Student).filter(Student.email == parsed['email']).one_or_none() is not None):
        return 'This user already exists', 400
    try:
        tutor = tutor_schema.load(parsed)
    except ValidationError as err:
        return "Invalid data", 400

    session.add(tutor)
    session.commit()
    return 'Token is given. Tutor is registered.'


@app.route('/tutor/<tutor_id>', methods=['DELETE'])
@auth.login_required
def delete_tutor(tutor_id):
    tutor = session.query(Tutor).filter(Tutor.id == tutor_id).one_or_none()
    if tutor is None:
        return 'The tutor doesn`t exist', 400
    if auth.current_user() != tutor.email:
        return 'You don`t have a permission to delete this tutor!', 401
    session.delete(tutor)
    session.commit()
    return 'The tutor is deleted'


@app.route('/student', methods=['POST'])
def create_student():
    student_data = request.json
    student_schema = StudentSchema()
    parsed = {
        'id': student_data['id'],
        'name': student_data['name'],
        'surname': student_data['surname'],
        'email': student_data['email'],
        'password': bcrypt.generate_password_hash(student_data['password']).decode('utf-8'),
        'age': student_data['age']
    }

    if (session.query(Tutor).filter(Tutor.email == parsed['email']).one_or_none() is not None) or \
            (session.query(Student).filter(Student.email == parsed['email']).one_or_none() is not None):
        return 'This user already exists', 400
    try:
        student = student_schema.load(parsed)
    except ValidationError as err:
        return "Invalid data", 400

    session.add(student)
    session.commit()
    return 'Token is given. Student is registered'


@app.route('/student/<student_id>', methods=['DELETE'])
@auth.login_required
def delete_student(student_id):
    student = session.query(Student).filter(Student.id == student_id).one_or_none()
    if student is None:
        return 'The student doesn`t exist', 400
    if auth.current_user() != student.email:
        return 'You don`t have a permission to delete this student!', 401
    session.delete(student)
    session.commit()
    return 'The student is deleted'


@app.route('/tutor/<tutor_id>/my_courses')
@auth.login_required
def show_tutor_courses(tutor_id):
    tutor = session.query(Tutor).filter(Tutor.id == tutor_id).one_or_none()

    if tutor is None:
        return 'The tutor doesn`t exist', 400

    if auth.current_user() != tutor.email:
        return 'You don`t have a permission to get information about courses of another tutor!', 401

    courses = session.query(Course).filter(Course.tutor_id == tutor_id)

    if courses:
        return jsonify(CourseSchema(many=True, exclude=['tutor_id']).dump(courses))
    else:
        return 'There is no courses'


@app.route('/student/<st_id>/my_courses')
@auth.login_required
def show_students_courses(st_id):
    student = session.query(Student).filter(Student.id == st_id).one_or_none()

    if student is None:
        return 'The student doesn`t exist', 400

    if auth.current_user() != student.email:
        return 'You don`t have a permission to get information about courses of this student!', 401

    my_courses =  session.query(Course).filter(Course.students.any(Student.id == st_id))

    if my_courses:
        return jsonify(CourseSchema(many=True).dump(my_courses))
    else:
        return 'There is no courses'


@app.route('/tutor/<tutor_id>/add', methods=['POST'])
@auth.login_required
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

    if auth.current_user() != tutor.email:
        return 'You don`t have a permission!', 401

    tutor_schema = TutorSchema(exclude=['password'])

    parsed = {
        'id': course_data['id'],
        'student_number': '0',
        'name': course_data['name'],
        'tutor_id': tutor_id,
        "students": [],
    }

    try:
        course = course_schema.load(parsed)
    except ValidationError as err:
        return err.messages, 400

    session.add(course)
    session.commit()
    return "Course is created"


@app.route('/tutor/<tutor_id>/update', methods=['PUT'])
@auth.login_required
def update_course(tutor_id):
    tutor_schema = TutorSchema()
    tutor = session.query(Tutor).filter(Tutor.id == tutor_id).one_or_none()

    try:
        tutor_schema.dump(tutor)
    except ValidationError as err:
        return 'invalid id', 400
    if tutor is None:
        return 'The tutor doesn`t exist', 404

    if auth.current_user() != tutor.email:
        return 'You don`t have a permission to update this course!', 401
    # if tutor_id

    course_data = request.json
    course_schema = CourseSchema()
    course = session.query(Course).filter(Course.id == course_data['id']).one_or_none()

    if course.tutor_id != tutor_id:
        return 'You don`t have a permission to update this course!', 401

    if course is None:
        return 'The course doesn`t exist', 404

    parsed = {
        'id': course_data['id'],
        'name': course_data['name'],
    }

    try:
        data = course_schema.load(parsed)
    except ValidationError as err:
        return err.messages, 400
    course.id = data.id
    course.name = data.name
    course.tutor_id = tutor_id
    session.commit()
    return course_schema.dump(course)


@app.route('/tutor/<tutor_id>/delete/<course_id>', methods=['DELETE'])
@auth.login_required
def delete_course(tutor_id, course_id):
    tutor_schema = TutorSchema()
    tutor = session.query(Tutor).filter(Tutor.id == tutor_id).one_or_none()

    try:
        tutor_schema.dump(tutor)
    except ValidationError as err:
        return 'invalid id', 400
    if tutor is None:
        return 'The tutor doesn`t exist', 404

    if auth.current_user() != tutor.email:
        return 'You don`t have a permission to delete this course!', 401

    course = session.query(Course).filter(Course.id == course_id).one_or_none()
    if course is None:
        return 'The course doesn`t exist', 400

    if int(course.tutor_id) != int(tutor_id):
        return 'You don`t have a permission to delete this course!', 401

    session.delete(course)
    session.commit()
    return 'The course is deleted'


@app.route('/student/<student_id>/request/<course_id>', methods=['POST'])
@auth.login_required
def create_request(student_id, course_id):

    student = session.query(Student).filter(Student.id == student_id).one_or_none()
    if student is None:
        return 'The student doesn`t exist', 400

    if auth.current_user() != student.email:
        return 'You don`t have a permission to create request!', 401

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
        'student_id': student_id,
        'course_id': course_id,
    }

    if not session.query(Request).filter(Request.id == temp_id).one_or_none() is None:
        return 'This request has been sent earlier. Wait for approving', 400
    try:
        request_course = request_schema.load(data)
    except ValidationError as err:
        return err.messages, 400

    session.add(request_course)
    session.commit()
    return 'Request has been sent'


@app.route('/tutor/<tutor_id>/request/<request_id>', methods=['PUT'])
@auth.login_required
def disapprove_request(tutor_id, request_id):
    tutor = session.query(Tutor).filter(Tutor.id == tutor_id).one_or_none()
    current_tutor = session.query(Tutor).filter(Tutor.email == auth.current_user()).one_or_none()
    if tutor is None:
        return 'The tutor doesn`t exist', 400

    if auth.current_user() != tutor.email:
        return 'You don`t have a permission to approve(disapprove) the request!', 401

    students_request = session.query(Request).filter(Request.id == request_id).one_or_none()
    if students_request is None:
        return 'The request doesn`t exist', 400

    parsed_status = request.json

    students_request.status = parsed_status['status'] if 'status' in parsed_status else students_request.status

    student = session.query(Student).filter(Student.id == students_request.student_id).one_or_none()

    current_course = session.query(Course).filter(Course.id == students_request.course_id).one_or_none()

    if int(current_course.tutor_id) != int(tutor_id):
        return 'You don`t have a permission to approve(disapprove) the request!', 401

    if parsed_status['status'] == 'approved':
        course = session.query(Course).filter(Course.id == students_request.course_id).one_or_none()
        course.student_number = course.student_number + 1
        course.students.append(student)

    session.commit()
    return 'Request is considered'


if __name__ == '__main__':
    app.run()
