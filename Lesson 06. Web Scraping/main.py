import requests

import time
from datetime import timedelta

from app import *
from custom import *


ENTRY_POINT = "https://openedu.ru/course"


def main():
    res = requests.get(ENTRY_POINT)
    text = res.text
    print("Started processing of html at <%s>" % ENTRY_POINT)

    specs = fetch_specializations(text)
    db.executemany("insert into specializations(id, code, title) values (?, ?, ?)", list(specs))
    print("Filled specializations table...")

    schools, sql = fetch_schools(text)
    db.executemany(sql, schools)
    print("Filled schools table...")

    instructors, sql = fetch_instructors(text)
    db.executemany(sql, instructors)
    print("Filled instructors table...")

    courses, sql, courses2specializations, courses2instructors = fetch_courses(text)
    db.executemany(sql, courses)
    print("Filled courses table...")

    db.executemany("insert into courses_specializations(course_id, specialization_id) values (?, ?)",
                   courses2specializations)
    db.executemany("insert into courses_instructors(course_id, instructor_id) values (?, ?)",
                   courses2instructors)
    print("Added many to many links...")
    
    print("Scraping finished.")


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print('Full execution time', timedelta(seconds=end - start))
