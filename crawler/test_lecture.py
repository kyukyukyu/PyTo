#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import crawler_config
from department import Department

dep = Department(u'의학과', u'H3HBDC')
dep.load_lectures()

for lecture in dep.lecture_group.iter_lectures():
    subject_code = lecture.data['subject_code']
    name = lecture.data['name']
    lecture_code = lecture.data['lecture_code']

    time = ''
    for entry in lecture.data['time']:
        time += str(entry)

    print '%s\t%s\t%s\t%s' % (subject_code, name, lecture_code, time)