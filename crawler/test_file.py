#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import codecs

if not os.path.isdir('./temp'):
    os.mkdir('temp')

with codecs.open('./temp/temp', encoding='utf-8', mode='w+') as f:
    f.write('hello world\n')
    f.write(u'한글도 잘 써지나요?')