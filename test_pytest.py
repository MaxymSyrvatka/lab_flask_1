from flask import json
import pytest
from .main import app
from base64 import b64encode

def create_tutor(client):
    client.post('/tutor', data=json.dumps({'id': '1', "name": "Test Tutor 1",
                "surname" : "Test Tutor Surname 1" , "email" : "email_tutor_1@gmail.com", "password" : "qwert12345", "age" : "30"}),
                content_type='application/json')

    client.post('/tutor', data=json.dumps({'id': '2', "name": "Test Tutor 2",
                                           "surname": "Test Tutor Surname 2", "email": "email_tutor_2@gmail.com",
                                           "password": "qwert12345", "age": "30"}),
                content_type='application/json')

    client.post('/tutor', data=json.dumps({'id': '3', "name": "Test Tutor 3",
                                           "surname": "Test Tutor Surname 3", "email": "email_tutor_3@gmail.com",
                                           "password": "qwert12345", "age": "30"}),
                content_type='application/json')


def create_student(client):
    client.post('/student', data=json.dumps({"id" : "1", "name": "test1", "surname":
                  "test1", "email": "test1@yugmail.com", "password" : "lsdchbvjbv", "age" : "17"}),
                content_type='application/json')

    client.post('/student', data=json.dumps({"id": "2", "name": "test2", "surname":
        "test2", "email": "test2@yugmail.com", "password": "lsdchbvjbv", "age": "17"}),
                content_type='application/json')

    client.post('/student', data=json.dumps({"id": "3", "name": "test3", "surname":
        "test1", "email": "test3@yugmail.com", "password": "lsdchbvjbv", "age": "17"}),
                content_type='application/json')

@pytest.fixture
def client():
    client = app.test_client()
    create_tutor(client)
    create_student(client)
    return client


def test_post_tutor(client):
    response1 = client.post(f'/tutor', content_type='application/json',
                            data=json.dumps({'id': '4', "name": "Test Tutor 4",
                                             "surname": "Test Tutor Surname 4", "email": "email_tutor_4@gmail.com",
                                             "password": "qwert12345", "age": "30"})).status_code

    assert response1 == 200
    response2 = client.post(f'/tutor', content_type='application/json', data=json.dumps({'id': '1', "name": "Test Tutor 1",
                "surname" : "Test Tutor Surname 1" , "email" : "email_tutor_1@gmail.com",
                 "password" : "qwert12345", "age": "30"})).status_code
    assert response2 == 400


def test_post_student(client):
    response1 = client.post(f'/student', content_type='application/json',
                            data=json.dumps({"id" : "4", "name": "test4", "surname":
                  "test4", "email": "test4@yugmail.com", "password" : "lsdchbvjbv", "age" : "17"})).status_code

    assert response1 == 200
    response2 = client.post(f'/student', content_type='application/json', data=json.dumps({"id" : "1", "name": "test1", "surname":
                  "test1", "email": "test1@yugmail.com", "password" : "lsdchbvjbv", "age" : "17"})).status_code
    assert response2 == 400


def test_get_tutor(client):
    credentials1 = b64encode(b'email_tutor_1@gmail.com:qwert12345').decode('utf-8')
    credentials2 = b64encode(b'test4@yugmail.com:lsdchbvjbv').decode('utf-8')
    response1 = client.get('/tutor/1', headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response1 == 200
    response2 = client.get('/tutor/5', headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response2 == 404
    response3 = client.get('/tutor/1', headers={'Authorization': f'Basic {credentials2}'}).status_code
    assert response3 == 401


def test_get_student(client):
    credentials1 = b64encode(b'test1@yugmail.com:lsdchbvjbv').decode('utf-8')
    credentials2 = b64encode(b'test4@yugmail.com:lsdchbvjbv').decode('utf-8')
    response1 = client.get('/student/1', headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response1 == 200
    response2 = client.get('/student/5', headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response2 == 404
    response3 = client.get('/student/1', headers={'Authorization': f'Basic {credentials2}'}).status_code
    assert response3 == 401


def test_delete_tutor(client):
    credentials1 = b64encode(b'email_tutor_1@gmail.com:qwert12345').decode('utf-8')
    credentials2 = b64encode(b'test4@yugmail.com:lsdchbvjbv').decode('utf-8')
    response2 = client.delete('/tutor/5', headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response2 == 400
    response3 = client.delete('/tutor/1', headers={'Authorization': f'Basic {credentials2}'}).status_code
    assert response3 == 401
    response1 = client.delete('/tutor/1', headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response1 == 200


def test_delete_student(client):
    credentials1 = b64encode(b'test1@yugmail.com:lsdchbvjbv').decode('utf-8')
    credentials2 = b64encode(b'test4@yugmail.com:lsdchbvjbv').decode('utf-8')
    response2 = client.delete('/student/5', headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response2 == 400
    response3 = client.delete('/student/1', headers={'Authorization': f'Basic {credentials2}'}).status_code
    assert response3 == 401
    response1 = client.delete('/student/1', headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response1 == 200

def test_get_tutors_course(client):
    credentials1 = b64encode(b'email_tutor_1@gmail.com:qwert12345').decode('utf-8')
    credentials2 = b64encode(b'test4@yugmail.com:lsdchbvjbv').decode('utf-8')
    response1 = client.get('/tutor/1/my_courses', headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response1 == 200
    response2 = client.get('/tutor/5/my_courses', headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response2 == 400
    response3 = client.get('/tutor/1/my_courses', headers={'Authorization': f'Basic {credentials2}'}).status_code
    assert response3 == 401


def test_get_student_courses(client):

    credentials1 = b64encode(b'test2@yugmail.com:lsdchbvjbv').decode('utf-8')
    credentials2 = b64encode(b'test4@yugmail.com:lsdchbvjbv').decode('utf-8')
    response1 = client.get('/student/2/my_courses', headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response1 == 200
    response2 = client.get('/student/5/my_courses', headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response2 == 400
    response3 = client.get('/student/2/my_courses', headers={'Authorization': f'Basic {credentials2}'}).status_code
    assert response3 == 401


def test_post_course(client):
    credentials1 = b64encode(b'email_tutor_2@gmail.com:qwert12345').decode('utf-8')
    credentials2 = b64encode(b'test4@yugmail.com:lsdchbvjbv').decode('utf-8')
    credentials3 = b64encode(b'email_tutor_3@gmail.com:qwert12345').decode('utf-8')
    tutor_id1 = 2
    tutor_id2 = 5
    tutor_id3 =3
    response1 = client.post(f'/tutor/{tutor_id1}/add',data=json.dumps({"id": "1", "name": "French"}),content_type='application/json',
                           headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response1 == 200
    response2 = client.post(f'/tutor/{tutor_id2}/add',data=json.dumps({'id' : "1", "name": "French"}), content_type='application/json',
                           headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response2 == 404
    response3 = client.post(f'/tutor/{tutor_id1}/add', data=json.dumps({'id': "1", "name": "French"}), content_type='application/json',
                           headers={'Authorization': f'Basic {credentials2}'}).status_code
    assert response3 == 401
    response4 = client.post(f'/tutor/{tutor_id3}/add', data=json.dumps({"id": "2", "name": "French"}),
                            content_type='application/json',
                            headers={'Authorization': f'Basic {credentials3}'}).status_code
    assert response4 == 200


def test_put_course(client):
    credentials1 = b64encode(b'email_tutor_2@gmail.com:qwert12345').decode('utf-8')
    credentials2 = b64encode(b'test4@yugmail.com:lsdchbvjbv').decode('utf-8')
    tutor_id1 = 2
    tutor_id2 = 5
    response1 = client.put(f'/tutor/{tutor_id1}/update',data=json.dumps({"id": "1", "name": "Ucr"}),content_type='application/json',
                           headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response1 == 200
    response2 = client.put(f'/tutor/{tutor_id2}/update',data=json.dumps({'id' : "1", "name": "French"}),content_type='application/json',
                           headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response2 == 404
    response3 = client.put(f'/tutor/{tutor_id1}/update', data=json.dumps({'id': "1", "name": "French"}),content_type='application/json',
                           headers={'Authorization': f'Basic {credentials2}'}).status_code
    assert response3 == 401
    response4 = client.put(f'/tutor/{tutor_id2}/update', data=json.dumps({'id': "4", "name": "French"}),content_type='application/json',
                           headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response4 == 404


def test_delete_course(client):
    credentials1 = b64encode(b'email_tutor_2@gmail.com:qwert12345').decode('utf-8')
    credentials2 = b64encode(b'test4@yugmail.com:lsdchbvjbv').decode('utf-8')
    tutor_id1 = 2
    tutor_id2 = 5

    response2 = client.delete(f'/tutor/{tutor_id2}/delete/1',
                           headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response2 == 404
    response3 = client.delete(f'/tutor/{tutor_id1}/delete/1',
                           headers={'Authorization': f'Basic {credentials2}'}).status_code
    assert response3 == 401
    response4 = client.delete(f'/tutor/{tutor_id1}/delete/9',
                           headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response4 == 400
    response5 = client.delete(f'/tutor/{tutor_id1}/delete/2',
                           headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response5 == 401
    response1 = client.delete(f'/tutor/{tutor_id1}/delete/1',
                           headers={'Authorization': f'Basic {credentials1}'}).status_code
    assert response1 == 200


def test_post_request(client):

    credentials2 = b64encode(b'test4@yugmail.com:lsdchbvjbv').decode('utf-8')
    credentials3 = b64encode(b'email_tutor_3@gmail.com:qwert12345').decode('utf-8')

    response1 = client.post(f'/student/4/request/2',
                           headers={'Authorization': f'Basic {credentials2}'}).status_code
    assert response1 == 200
    response2 = client.post(f'/student/4/request/2',
                            headers={'Authorization': f'Basic {credentials3}'}).status_code
    assert response2 == 401
    response3 = client.post(f'/student/10/request/2',
                            headers={'Authorization': f'Basic {credentials2}'}).status_code
    assert response3 == 400
    response3 = client.post(f'/student/4/request/5',
                            headers={'Authorization': f'Basic {credentials2}'}).status_code
    assert response3 == 400
    response4 = client.post(f'/student/4/request/2',
                            headers={'Authorization': f'Basic {credentials2}'}).status_code
    assert response4 == 400


def test_put_request(client):

    credentials2 = b64encode(b'test4@yugmail.com:lsdchbvjbv').decode('utf-8')
    credentials3 = b64encode(b'email_tutor_3@gmail.com:qwert12345').decode('utf-8')
    credentials4 = b64encode(b'email_tutor_4@gmail.com:qwert12345').decode('utf-8')

    response1 = client.put(f'/tutor/3/request/42',data=json.dumps({'status': "approved"}),content_type='application/json',
                           headers={'Authorization': f'Basic {credentials3}'}).status_code
    assert response1 == 200
    response2 = client.put(f'/tutor/50/request/42', data=json.dumps({'status': "uapproved"}),
                            content_type='application/json',
                            headers={'Authorization': f'Basic {credentials3}'}).status_code
    assert response2 == 400
    response3 = client.put(f'/tutor/3/request/50', data=json.dumps({'status': "approved"}),
                            content_type='application/json',
                            headers={'Authorization': f'Basic {credentials3}'}).status_code
    assert response3 == 400
    response4 = client.put(f'/tutor/3/request/42', data=json.dumps({'status': "approved"}),
                            content_type='application/json',
                            headers={'Authorization': f'Basic {credentials2}'}).status_code
    assert response4 == 401
    response5 = client.put(f'/tutor/4/request/42', data=json.dumps({'status': "approved"}),
                            content_type='application/json',
                            headers={'Authorization': f'Basic {credentials4}'}).status_code
    assert response5 == 401
