#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import crawler_config
from lecture import CulturalLecture
from area_collector import AreaCollector

a_c = AreaCollector()
CulturalLecture.area_collector = a_c
lec1 = CulturalLecture({
    'subject_code': 'GEN703',
    'name': u'창의와소통',
    'instructor': u'성태현',
    'lecture_code': '13131',
    'category': u'핵심교양',
    'year': '',
    'score': '2.00'
})

area_list = a_c.area_list
for area in area_list:
    print area