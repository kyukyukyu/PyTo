#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import urllib
import urllib2
from config import crawler_config

URL_DEPARTMENT_LIST = 'http://ezhub.hanyang.ac.kr/haksa/'
URL_DEPARTMENT_LIST += 'hus/sooup/SooUp_ret.jsp'
UNDERGRADUATE_JOJIK = 3

class DepartmentLoader(object):

    def __init__(self):
        self.departments = []
        self.index = 0

    # method for preparing soup object
    def prepare_soup(self):
        # prepare query string in dictionary type
        query = {}
        config = crawler_config
        query['level'] = 1
        query['data'] = ''
        query['data2'] = config['year']
        query['data3'] = config['term'] * 10
        query['data4'] = config['campus'] + str(UNDERGRADUATE_JOJIK)

        url = URL_DEPARTMENT_LIST + '?' + urllib.urlencode(query)
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, 'lxml', from_encoding='euc-kr')

        return soup

    def __iter__(self):
        soup = self.prepare_soup()
        dep_list = soup.find('select', attrs={'name': 'data_hakgwa'})

        str_regex = u'([\w가-힣· ]+\(?[\w가-힣· ]+\)?[\w가-힣· ]*)\(([가-힣· ]+)'
        regex = re.compile(str_regex)

        del self.departments[:]

        for dep in dep_list.find_all('option'):
            str_dep = dep.string
            match = regex.match(str_dep)

            if match == None:
                continue

            dep_name = match.group(1)
            dep_code = dep['value'].rstrip()

            self.departments.append((dep_name, dep_code))

        del soup

        return self

    def next(self):
        if self.index >= len(self.departments):
            raise StopIteration
        else:
            self.index += 1
            return self.departments[self.index - 1]
