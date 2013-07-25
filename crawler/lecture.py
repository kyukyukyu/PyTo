#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import urllib2
from config import crawler_config

URL_SYLLABUS = 'https://ezhub.hanyang.ac.kr/haksa/hus/sooup/Sooup_pvi_v1.jsp'
URL_SEARCH_SUBJECT = 'https://ezhub.hanyang.ac.kr/guest/haksa/'
URL_SEARCH_SUBJECT += 'gyogwa/GyoGwa_v.jsp'
UNDERGRADUATE_JOJIK = 3
SUBJECT_LIST_HEAD_CELL_CLASS = 'LTBHTR1'
SUBJECT_LIST_COL_DICT = {
    'subject_code': 0,
    'category': 2,
    'area': 3
}

# method for providing the number of day of week
def num_of_day(day_char):
    if day_char == u'월':
        return 1
    elif day_char == u'화':
        return 2
    elif day_char == u'수':
        return 3
    elif day_char == u'목':
        return 4
    elif day_char == u'금':
        return 5
    elif day_char == u'토':
        return 6
    else:
        return 0

# method for providing the number of time in a week
# for example, num_of_time('09:00', 3) is 303
def num_of_time(str_time, n_day):
    numbers = str_time.split(':')
    hour = int(numbers[0])
    minute = int(numbers[1])

    return n_day * 100 + (hour - 8) * 2 + (minute / 30) + 1

class Lecture(object):

    def __init__(self, data):
        self.data = dict(data)
        self.data['time'] = []
        self.load_time()

    # method for preparing time string
    def prepare_time(self):
        # prepare query string in dictionary type
        query = {}
        config = crawler_config
        query['year'] = config['year']
        query['term'] = config['term'] * 10
        query['suup_cd'] = self.data['lecture_code']

        url = URL_SYLLABUS + '?' + urllib.urlencode(query)
        page = urllib2.urlopen(url)

        if config['debug']:
            print self.data['name'] + u'(' + self.data['lecture_code'] + u') 수업개요서 읽음'

        for line in page:
            utf8_line = line.decode('euc-kr').encode('utf-8')
            if '<td class="FTBHTD2">강의시간</td>' in utf8_line:
                line_time = page.next().decode('euc-kr').encode('utf-8')
                soup = BeautifulSoup(line_time)
                str_time = soup.string
                del soup

                if str_time == None:
                    return ''
                else:
                    return str_time

        return ''

    # method for loading time information of the lecture
    def load_time(self):
        str_time = self.prepare_time()
        str_time = str_time.replace(' ', '')    # remove spaces

        if crawler_config['debug']:
            print self.data['name'] + u' 수업시간: ' + str_time
        
        if str_time == '':
            return

        info_chunks = str_time.split(',')
        for chunk in info_chunks:
            # chunks is a merely temporary variable
            # following statement splits the string like
            # '월(09:00-10:30)/H77-501' -> ['월(09:00-10:30)', 'H77-501']
            chunks = chunk.split('/', 1)
            time = chunks[0]
            if len(chunks) == 2:
                room = chunks[1]
            else:
                room = ''

            # following statement splits the string like
            # '월(09:00-10:30)' -> ['월', '09:00-10:30)']
            chunks = time.split('(')
            day_of_week = num_of_day(chunks[0])

            # following statement splits the string like
            # '09:00-10:30)' -> ['09:00', '10:30']
            chunks = chunks[1][:-1].split('-')

            # following statements convert string to time number
            # '09:00', Monday -> 103
            if chunks[0] != '':     # in case of no start time
                start_time = num_of_time(chunks[0], day_of_week)
            else:
                start_time = day_of_week * 100 + 1

            if chunks[1] != '':     # in case of no end time
                end_time = num_of_time(chunks[1], day_of_week)
            else:
                end_time = day_of_week * 100 + 32

            time_entry = {}
            time_entry['start'] = start_time
            time_entry['end'] = end_time
            time_entry['room'] = room

            self.data['time'].append(time_entry)

class CulturalLecture(Lecture):

    def __init__(self, data):
        super(CulturalLecture, self).__init__(data)
        self.load_area()

    # method for preparing area soup object
    def prepare_area_soup(self):
        # prepare query string in dictionary type
        query = {}
        config = crawler_config
        query['jojik'] = config['campus'] + str(UNDERGRADUATE_JOJIK)
        query['gwajung'] = config['course']
        query['hakyun'] = ''
        name = self.data['name'].encode('euc-kr')
        query['gwamok'] = name

        url = URL_SEARCH_SUBJECT + '?' + urllib.urlencode(query)
        url += '&gwanjang=%'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, 'lxml', from_encoding='euc-kr')

        if config['debug']:
            print self.data['name'] + u'(' + self.data['lecture_code'] + u') 교양영역 찾음'

        return soup

    # method for preparing table rows object
    def prepare_subject_rows(self, soup):
        table_head_cell = soup.select('td.' + SUBJECT_LIST_HEAD_CELL_CLASS)[0]
        table_body = table_head_cell.parent.parent
        table_rows = table_body.find_all('tr')

        return table_rows[1:]

    # method that loads the area of lecture
    def load_area(self):
        soup = self.prepare_area_soup()
        table_rows = self.prepare_subject_rows(soup)

        for row in table_rows:
            cells = row.find_all('td')
            subject_data = {}

            subject_data['subject_code'] = \
                cells[SUBJECT_LIST_COL_DICT['subject_code']].string
            subject_data['category'] = \
                cells[SUBJECT_LIST_COL_DICT['category']].string

            is_equal = True

            for k, v in subject_data.iteritems():
                is_equal &= (v == self.data[k])

            if is_equal:
                self.area_str = cells[SUBJECT_LIST_COL_DICT['area']].string
                if crawler_config['debug']:
                    print self.data['name'] + u'(' + self.data['lecture_code'] + \
                          u') 교양영역: ' + self.area_str
                break

        del soup
