# -*- coding:utf-8 -*-
import pymysql
import configparser
import logging
from DBUtils.PooledDB import PooledDB
__author__ = 'JackGao'


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')


