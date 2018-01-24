# -*- coding:utf-8 -*-
from src import pool, dbpool
import threading
import logging
import time
__author__ = 'JackGao'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
# init thread pool
thread_pool = pool.ThreadPool(2)
# init db pool
db_pool = dbpool.db_pool

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
        cursor = conn.cursor()
        sql = 'insert into info( song_name, singer_name, pub_time, rating_num) values(%s, %s, %s, %s)'
        cursor.executemany(sql, data)
        conn.commit()
        logging.debug("Insert Finished")
    finally:
        cursor.close()
        conn.close()


def main(tp):
    data_list = tp.data_list
    while loop:
        logging.debug("******The data_list has %d record*****" % len(data_list))
        if len(data_list) >= 100:
            tp.lock_list.acquire()
            try:
                insert_list = data_list[:]
                data_list.clear()
            finally:
                tp.lock_list.release()
            logging.debug("Create Thread to insert data... size[%d] " % len(insert_list))
            db_thread = threading.Thread(target=insert_data, args=(insert_list,))
            db_thread.start()
        time.sleep(1)


main_thread = threading.Thread(target=main, args=(thread_pool,))
main_thread.start()

