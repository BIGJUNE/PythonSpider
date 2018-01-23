# -*- coding:utf-8 -*-
from src import dao, pool, dbpool
import threading
import logging
import time
__author__ = 'JackGao'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
# init thread pool
thread_pool = pool.ThreadPool(4)
# init db pool
db_pool = dbpool.db_pool
# get thread lock
lock_list = thread_pool.lock_data_list
data_list = thread_pool.data_list

loop = True
logging.debug("Start the thread pool")
# start thread to download html page
tp_thread = threading.Thread(target=thread_pool.start)
tp_thread.start()


def insert_data(data=[]):
    # Insert data into database
    # Function accept a list as parameter
    if len(data) == 0:
        return 0
    conn = db_pool.get_connect()
    try:
        logging.debug("size = %d ready to insert" % len(data))
        with conn.cursor() as cursor:
            sql = 'insert into info(content, comment_time, user_name) values(%s, %s, %s)'
            cursor.executemany(sql, data)
            conn.commit()
        logging.debug("Insert Finished")
    finally:
        conn.close()


while loop:
    if len(data_list) >= 1000:
        lock_list.acquire()
        try:
            insert_list = data_list[:]
            data_list.clear()
            logging.debug("Create Thread to insert data... size[%d] " % len(insert_list))
            db_thread = threading.Thread(target=insert_data, args=(insert_list,))
            db_thread.start()
        finally:
            lock_list.release()
    time.sleep(1)
