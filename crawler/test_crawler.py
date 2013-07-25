#!/usr/bin/python
# -*- coding: utf-8 -*-

from crawler import LectureCrawler

crawler = LectureCrawler()
crawler.crawl()

for major_lecture_group in crawler.iter_major_lecture_groups():
    print major_lecture_group.name

for cultural_lecture_group in crawler.iter_cultural_lecture_groups():
    print cultural_lecture_group.name