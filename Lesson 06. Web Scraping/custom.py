import json
import random
import re

import aiohttp
import asyncio
from bs4 import BeautifulSoup

BASE_URL = "https://openedu.ru"

SPECIALIZATIONS_RE = r"GROUPS = (\{.*\});"
SCHOOLS_RE = r"UNIVERSITIES = (\{.*\});"
COURSES_RE = r"COURSES = (\{.*\});"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0"
REQUEST_HEADERS = {"User-Agent": USER_AGENT}
SCHOOL_INSTRUCTORS_URL_TEMPLATE = BASE_URL + "/university/%s/?load=get_other_teachers"


def fetch_specializations(text):
    match = re.search(SPECIALIZATIONS_RE, text)
    raw_json = match.group(1)
    specs = json.loads(raw_json)
    data = set()
    for k, v in specs.items():
        data.add((k, v['code'], v['title']))
    return data


async def fetch(session, url, random_delay=False):
    if random_delay:
        current_delay = random.randrange(0, 45)
        print("Parse url with delay {:0>2d}".format(current_delay), url)
        await asyncio.sleep(current_delay)

    async with session.get(url) as response:
        if response.status != 200:
            print("Response error at", url)
            response.raise_for_status()
        return await response.text()


async def start_async_fetch(urls, random_delay=False):
    async with aiohttp.ClientSession(headers=REQUEST_HEADERS) as session:
        results = await asyncio.gather(*[asyncio.create_task(fetch(session, url, random_delay)) for url in urls])
    return results


def extract_school_info(text):
    soup = BeautifulSoup(text, 'lxml')
    result = {
        'title': soup.select_one(".personal-info h1").contents[0],
        'description': inner_html(soup.select_one("#about"))
    }

    school_site_tag = soup.select_one(".info-card a")
    result['school_site'] = school_site_tag['href'] if school_site_tag else None

    return result


def inner_html(tag):
    return "".join([str(x) for x in tag.contents])


def _extract_school_slug_2_id(text):
    match = re.search(SCHOOLS_RE, text)
    raw_json = match.group(1)
    slug2id = dict()
    schools_info = json.loads(raw_json)

    for key, val in schools_info.items():
        slug2id[val['slug']] = key

    return slug2id


def fetch_instructors(text):
    slug2id = _extract_school_slug_2_id(text)

    ret = []

    urls = [SCHOOL_INSTRUCTORS_URL_TEMPLATE % k for k in slug2id.keys()]

    loop = asyncio.get_event_loop()
    html_documents = loop.run_until_complete(start_async_fetch(urls))

    for school_id, html in zip(list(slug2id.values()), html_documents):
        instructors = extract_istructors_info(html, school_id)
        ret.extend(instructors)

    sql = "insert into instructors(id, name, education_level, post, school_id) values (?, ?, ?, ?, ?)"

    return ret, sql


def extract_istructors_info(html, school_id):
    instructors = []

    soup = BeautifulSoup(html, 'lxml')

    tags = soup.select('.card-lecturer')

    for instructor_tag in tags:
        link = instructor_tag.select_one("h3 a")
        id = int(re.findall("\d+", link["href"])[0])
        name = link.contents[0].strip()
        education_level = instructor_tag.select_one('.instructor-post').contents[0].strip()
        post = instructor_tag.select_one('.instructor-post span').next_sibling.strip()

        instructors.append((id, name, education_level, post, school_id))

    return instructors


def extract_course_info(html):
    course_info = dict()

    soup = BeautifulSoup(html, 'lxml')

    course_info['instructor_ids'] = [int(re.findall("\d+", link["href"])[0])
                                     for link in
                                     soup.select('.card-lecturer h3 a')]

    descr_tag = soup.select_one(".course-descr-data .issue")
    to_remove = descr_tag.select(".visible-xs-block, .local-tabs, .course_groups-box")
    for tag in to_remove:
        tag.decompose()

    course_info['description'] = inner_html(descr_tag)

    return course_info


def fetch_schools(text):
    match = re.search(SCHOOLS_RE, text)
    raw_json = match.group(1)
    schools = dict()
    schools_info = json.loads(raw_json)

    for key, val in schools_info.items():
        schools[key] = {
            'id': key,
            'slug': val['slug'],
            'url': val['url'],
            'abbr': val['abbr'],
            'title': None,
            'school_site': None,
            'description': None
        }

    urls = []
    for school in schools.values():
        urls.append(BASE_URL + school['url'])

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(start_async_fetch(urls))

    for key, school_html in zip(list(schools.keys()), results):
        data = extract_school_info(school_html)
        schools[key]['title'] = data['title']
        schools[key]['school_site'] = data['school_site']
        schools[key]['description'] = data['description']

    ret = []
    for school in schools.values():
        ret.append((school['id'], school['slug'], school['url'], school['abbr'],
                    school['title'], school['school_site'], school['description']))

    sql = "insert into schools(id, slug, url, abbr, title, school_site, description) values (?, ?, ?, ?, ?, ?, ?)"

    return ret, sql


def school_slug_by_url(url):
    m = re.match("^/course/(\w+)/", url)
    return m.group(1)


def fetch_courses(text):
    courses = []
    courses2specializations = []
    courses2instructors = []

    school_slug_to_id = _extract_school_slug_2_id(text)

    match = re.search(COURSES_RE, text)
    raw_json = match.group(1)
    tmp = json.loads(raw_json)

    courses_dict = dict()

    urls = []

    for key, val in tmp.items():
        status = None
        if len(val['sessions']) > 0:
            status = val['sessions'][0]['status']

        url = val['url']

        courses_dict[key] = {
            'id': int(key),
            'status': status,
            'weeks': int(val['weeks']) if val['weeks'] else None,
            'url': url,
            'title': val['title'],
            'school_id': school_slug_to_id[school_slug_by_url(url)],
            'description': None
        }

        courses2specializations.extend([(key, g) for g in val['groups']])
        urls.append(BASE_URL + url)

    loop = asyncio.get_event_loop()
    html_documents = loop.run_until_complete(start_async_fetch(urls, random_delay=True))

    for course_id, html in zip(list(courses_dict.keys()), html_documents):
        course_extra_data = extract_course_info(html)
        courses2instructors.extend([(course_id, g) for g in course_extra_data['instructor_ids']])
        courses_dict[course_id]['description'] = course_extra_data['description']

    for c in courses_dict.values():
        courses.append((c['id'], c['title'], c['weeks'], c['description'], c['status'], c['url'], c['school_id']))

    sql = "insert into courses(id, title, weeks, description, status, url, school_id) values (?, ?, ?, ?, ?, ?, ?)"

    return courses, sql, courses2specializations, courses2instructors
