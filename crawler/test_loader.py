#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import crawler_config
from department_loader import DepartmentLoader

dep_dict = {}

for name, code in DepartmentLoader():
    code_prefix = code[:4]

    if code_prefix not in dep_dict:
        dep_dict[code_prefix] = []

    dep_dict[code_prefix].append(name)

def print_list(l):
    s = ''

    for entry in l:
        s += entry + ', '

    return s

for k, v in dep_dict.iteritems():
    print k + ': ' + print_list(v)