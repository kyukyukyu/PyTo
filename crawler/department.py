#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import urllib2
from config import crawler_config
from lecture import Lecture, CulturalLecture
from dep_utils import LectureGroup

URL_LECTURE_LIST = "https://ezhub.hanyang.ac.kr/haksa/hus/sooup/Sooup_v1.jsp"
UNDERGRADUATE_JOJIK = 3
LECTURE_LIST_HEAD_CELL_CLASS = 'LTBHTR1'
LECTURE_LIST_COL_DICT = {
    'subject_code': 0,
    'name': 1,
    'instructor': 2,
    'lecture_code': 3,
    'category': 5,
    'year': 6,
    'score': 8
}

class Department(object):

    def __init__(self, name, code):
        self.lecture_group = LectureGroup(name)
        self.name = name
        self.code = code
        self.lecture_class = Lecture

    # method for preparing soup object
    def prepare_soup(self):
        # prepare query string in dictionary type
        query = {}
        config = crawler_config
        query['year'] = config['year']
        query['term'] = config['term'] * 10
        query['campus'] = config['campus']
        query['jojik'] = UNDERGRADUATE_JOJIK
        query['hakgwa_cd'] = self.code

        url = URL_LECTURE_LIST + '?' + urllib.urlencode(query)
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, 'lxml', from_encoding='euc-kr')

        if config['debug']:
            print self.name + u' 수업목록 읽음'

        return soup

    # method for preparing table rows object
    def prepare_rows(self, soup):
        table_head_cell = soup.select('td.' + LECTURE_LIST_HEAD_CELL_CLASS)[0]
        table_body = table_head_cell.parent.parent
        table_rows = table_body.find_all('tr')

        # if no lecture
        if len(table_rows[1].find_all('td')) == 1:
            return []
        else:
            return table_rows[1:]

    # method for adding a lecture
    def add_lecture(self, lecture):
        self.lecture_group.add_lecture(lecture)

    # method that loads lectures of the department
    def load_lectures(self):
        soup = self.prepare_soup()
        table_rows = self.prepare_rows(soup)
        lecture_class = self.lecture_class

        for row in table_rows:
            cells = row.find_all('td')
            lecture_data = {}

            for k, v in LECTURE_LIST_COL_DICT.iteritems():
                lecture_data[k] = cells[v].string

            self.add_lecture(lecture_class(lecture_data))

        del soup

class UndergraduateDepartment(Department):

    def __init__(self, name, code):
        super(UndergraduateDepartment, self).__init__(name, code)
        self.lecture_class = CulturalLecture
        self.lectures_by_area = {}

    def add_lecture(self, lecture):
        area_str = lecture.area_str
        
        super(UndergraduateDepartment, self).add_lecture(lecture)
        
        lectures_by_area = self.lectures_by_area

        if area_str not in lectures_by_area:
            lectures_by_area[area_str] = LectureGroup(area_str)
        
        lectures_by_area[area_str].add_lecture(lecture)

    def iter_lecture_groups(self):
        for lecture_group in self.lectures_by_area.viewvalues():
            yield lecture_group
