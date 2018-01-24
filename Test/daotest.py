# -*- coding:utf-8 -*-
import unittest
import datetime


class TestDao(unittest.TestCase):

    def test_batchinsert(self):
        t1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        r1 = ('中國龍', t1, 'www.baidu.com')
        t2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        r2 = ('batchtest2', t2, 'www.baidu.com')
        t3 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        r3 = ('batchtest3', t3, 'www.baidu.com')
        t4 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        r4 = ('batchtest4', t4, 'www.baidu.com')
        rows = [r1, r2, r3, r4]
        # dao.insert_data(rows)
