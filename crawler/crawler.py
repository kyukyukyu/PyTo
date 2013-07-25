#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import crawler_config
from department_loader import DepartmentLoader
from department import Department, UndergraduateDepartment

class LectureCrawler(object):

    def __init__(self):
        self.departments = []           # list of departments
        self.ug_department = None       # undergraduate department

    # method for crawling
    def crawl(self):
        for dep_name, dep_code in DepartmentLoader():
            # if the department is 'undergraduate' department,
            # wrap the department with UndergraduateDepartment class object
            if len(dep_code) == 2:
                dep_obj = UndergraduateDepartment(name=dep_name,
                                                  code=dep_code)
                self.ug_department = dep_obj
            else:
                dep_obj = Department(name=dep_name, code=dep_code)
                self.departments.append(dep_obj)

            dep_obj.load_lectures()

    def iter_departments(self):
        for dep in self.departments:
            yield dep

    def iter_major_lecture_groups(self):
        for dep in self.departments:
            yield dep.lecture_group

    def iter_cultural_lecture_groups(self):
        return self.ug_department.iter_lecture_groups()