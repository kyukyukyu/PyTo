#!/usr/bin/python
# -*- coding: utf-8 -*-

from crawler import LectureCrawler
import os
import codecs

BATTO_FILE_PREFIX = 'db'
BATTO_FILE_EXTENSION = 'tdb'
BATTO_FILE_EXTENSION_2 = 'info'
BATTO_DIR = './tdb/'
DEBUG = False

crawler = LectureCrawler()
crawler.crawl()

colleges = {
    u'H3IA': u'정책과학대학',
    u'H3HX': u'융합전공',
    u'H3HW': u'경제금융대학',
    u'H3': u'서울 대학',
    u'H3HU': u'국제학부',
    u'H3HT': u'생활과학대학',
    u'H3HR': u'경영대학',
    u'H3HP': u'법학과',
    u'H3HN': u'자연과학대학',
    u'H3HM': u'사회과학대학',
    u'H3HL': u'인문과학대학',
    u'H3IB': u'예술·체육대학',
    u'H3HH': u'음악대학',
    u'H3HG': u'사범대학',
    u'H3HB': u'의과대학',
    u'H3HA': u'공과대학',
    u'H3IC': u'간호학부',
    u'Y3Y3': u'예체능대학',
    u'Y3YX': u'융합전공 (디자인공학)',
    u'Y3YF': u'경상대학',
    u'Y3YE': u'언론정보대학',
    u'Y3YD': u'국제문화대학',
    u'Y3YA': u'공학대학',
    u'Y3YO': u'과학기술대학',
    u'Y3YS': u'디자인대학',
    u'Y3': u'ERICA 대학',
    u'Y3YL': u'약학대학'
}

day_of_week = ['', u'월', u'화', u'수', u'목', u'금', u'토']

def str_time(time_num):
    time_num %= 100
    hour = (time_num - 1) / 2 + 8
    minute = ((time_num - 1) % 2) * 30
    return '%02d' % hour + ':' + '%02d' % minute

def get_time_info(time_entries):
    time_list = []
    time_str_list = []
    room_list = []

    for entry in time_entries:
        time = entry['start']
        time_str = day_of_week[time / 100] + '(' + str_time(time)
        end_time = entry['end']
        time_str += '-' + str_time(end_time) + ')'

        while time < end_time:
            time_list.append(time)
            time += 1

        time_str_list.append(time_str)
        room_list.append(entry['room'])

    return tuple([','.join([unicode(y) for y in x]) \
                 for x in [time_list, time_str_list, room_list]])

def write_lectures(f, lecture_group):
    for lecture in lecture_group.iter_lectures():
        # year, subject_code, lecture_code,
        # name, score, time_str, time, room, instructor
        line_format = '%s\t%s\t%d\t'
        line_format += '%s\t%d\t%s\t%s\t%s\t%s\n'

        time, time_str, room = get_time_info(lecture.data['time'])
        if lecture.data['year'] is None:
            year = ''
        else:
            year = str(lecture.data['year'])

        line = line_format % ( \
                   year, lecture.data['subject_code'], \
                   int(lecture.data['lecture_code']), lecture.data['name'], \
                   int(float(lecture.data['score'])), time_str, time, \
                   room, lecture.data['instructor'])

        f.write(line)

# check if the directory exists, and if not, create the directory
if not os.path.isdir(BATTO_DIR):
    os.mkdir(BATTO_DIR)

departments = []
i = 0

for department in crawler.iter_departments():
    name = department.name
    code = department.code
    college_str = colleges[code[:4]]
    
    file_index = '%03d' % i
    filename = BATTO_FILE_PREFIX + file_index + '.' + BATTO_FILE_EXTENSION

    if DEBUG:
        print filename + u' 쓰는 중...'

    with codecs.open(BATTO_DIR + filename, encoding='euc-kr', mode='w+') as f:
        f.write(college_str + '\n')
        f.write(name + '\n')

        write_lectures(f, department.lecture_group)

    departments.append((i, name))
    i += 1

areas = []

for cultural_lecture_group in crawler.iter_cultural_lecture_groups():
    name = cultural_lecture_group.name

    file_index = '%03d' % i
    filename = BATTO_FILE_PREFIX + file_index + '.' + BATTO_FILE_EXTENSION

    if DEBUG:
        print filename + u' 쓰는 중...'

    with codecs.open(BATTO_DIR + filename, encoding='euc-kr', mode='w+') as f:
        f.write((name + '\n') * 2)

        write_lectures(f, cultural_lecture_group)

    areas.append((i, name))
    i += 1

areas.sort(None, lambda x : x[1])

filepath = BATTO_DIR + BATTO_FILE_PREFIX + '.' + BATTO_FILE_EXTENSION_2
with codecs.open(filepath, encoding='euc-kr', mode='w+') as f:
    for department in departments:
        f.write('%d\t%c\t%s\n' % (department[0], 'M', department[1]))

    for area in areas:
        f.write('%d\t%c\t%s\n' % (area[0], 'G', area[1]))