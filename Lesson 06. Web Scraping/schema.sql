drop table if exists specializations;
create table specializations (
    id integer PRIMARY KEY,
    code text,
    title text
);

drop table if exists statuses;
create table statuses (
    slug text PRIMARY KEY,
    title text
);

drop table if exists schools;
create table schools (
    id integer PRIMARY KEY,
    slug text,
    title text,
    url text,
    abbr text,
    school_site text,
    description text
);

drop table if exists instructors;
create table instructors (
    id integer PRIMARY KEY,
    name text,
    education_level text,
    post text,
    school_id integer NOT NULL,
    FOREIGN KEY (school_id) REFERENCES school(id)
);

drop table if exists courses;
CREATE TABLE courses (
    id integer PRIMARY KEY,
    title text NOT NULL,
    weeks integer,
    description text,
    status text,
    url text,
    school_id integer not null,
    FOREIGN KEY (school_id) REFERENCES school(id)
);

drop table if exists courses_specializations;
CREATE TABLE courses_specializations (
        course_id INTEGER,
        specialization_id INTEGER,
        FOREIGN KEY(course_id) REFERENCES courses(id),
        FOREIGN KEY(specialization_id) REFERENCES specializations(id)
);

drop table if exists courses_instructors;
CREATE TABLE courses_instructors (
        course_id INTEGER,
        instructor_id INTEGER,
        FOREIGN KEY(course_id) REFERENCES courses(id),
        FOREIGN KEY(instructor_id) REFERENCES instructors(id)
);
