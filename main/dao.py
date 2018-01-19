# -*- coding:utf-8 -*-
import pymysql
import configparser
__author__ = 'JackGao'

# 初始化数据库连接并返回


def init_connect():

    # 读取配置文件
    config = configparser.ConfigParser()
    config.read('conf.ini')
    db_config = config['mysql']

    # 连接MySQL
    conn = pymysql.connect(host=db_config['host'],
                           port=int(db_config['port']),
                           user=db_config['user'],
                           password=db_config['password'],
                           db=db_config['db'],
                           charset=db_config['charset'],
                           cursorclass=pymysql.cursors.DictCursor)

    return conn


# 插入数据函数 接收一个Tuple构成的list作为参数


def insert_data(data=[]):
    conn = init_connect()
    try:
        with conn.cursor() as cursor:
            sql = 'insert into info(content, creep_time, source_page) values(%s, %s, %s)'
            cursor.executemany(sql, data)
            conn.commit()

    finally:
        conn.close()
