#!/usr/bin/python
# -*- coding: utf-8 -*-
from lecture import Lecture

class LectureGroup(object):
    
    def __init__(self, name):
        self.name = name
        self.lectures = []

    def add_lecture(self, lecture):
        if not isinstance(lecture, Lecture):
            raise TypeError('lecture is not an object of CulturalLecture')

        self.lectures.append(lecture)

    def iter_lectures(self):
        for lecture in self.lectures:
            yield lecture