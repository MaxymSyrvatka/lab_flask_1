from marshmallow import Schema, fields, post_load, validate
from models import Student, Tutor, Course, RequestStatus, Request


class StudentSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str()
    surname = fields.Str()
    email = fields.Email()
    password = fields.Str()
    age = fields.Int()

    @post_load
    def student_create(self, data, **kwargs):
        return Student(**data)



class TutorSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str()
    surname = fields.Str()
    email = fields.Email()
    password = fields.Str()
    age = fields.Int()

    @post_load
    def tutor_create(self, data, **kwargs):
        return Tutor(**data)


class CourseSchema(Schema):
    id = fields.Int(required=True)
    student_number = fields.Int()
    name = fields.Str()
    tutor_id = fields.Int()
    # tutor = fields.Nested(TutorSchema)
    #students = fields.List(fields.Nested(StudentSchema, only=["id"]))
    students = fields.List(fields.Nested(StudentSchema(only=["id"])))
    #students = fields.List(fields.Int())

    @post_load
    def course_create(self, data, **kwargs):
        return Course(**data)

class RequestSchema(Schema):
    id = fields.Int(required=True)
    status = fields.Str(validate = validate.OneOf(["placed", "approved", "disapproved"]))
    student_id = fields.Int()
    course_id = fields.Int()

    @post_load
    def request_create(self, data, **kwargs):
        return Request(**data)
