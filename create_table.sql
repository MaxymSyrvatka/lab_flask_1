CREATE TABLE student(
  id INTEGER,
  name VARCHAR,
  surname VARCHAR,
  email VARCHAR,
  password VARCHAR,
  age INTEGER,
  PRIMARY KEY (id)
);
CREATE TABLE tutor(
  id INTEGER,
  name VARCHAR,
  surname VARCHAR,
  email VARCHAR,
  password VARCHAR,
  age INTEGER,
  PRIMARY KEY (id)
);
CREATE TABLE course(
  id INTEGER,
  name VARCHAR,
  tutor_id INTEGER,
  student_number INTEGER,
--  students VARCHAR,
  PRIMARY KEY (id),
  FOREIGN KEY (tutor_id) REFERENCES tutor(id)

);
CREATE TABLE request(
  id INTEGER,
  student_id INTEGER,
  course_id INTEGER,
  status VARCHAR,
  PRIMARY KEY (id),
  FOREIGN KEY (student_id) REFERENCES student (id),
  FOREIGN KEY (course_id) REFERENCES course (id)
);

CREATE TABLE students_in_course(

  student_id INTEGER,
  course_id INTEGER,
  FOREIGN KEY (student_id) REFERENCES student (id),
  FOREIGN KEY (course_id) REFERENCES course (id)
);


