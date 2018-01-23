# -*- coding:utf-8 -*-
import threading
from src import net
import time
import logging
__author__ = 'JackGao'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')


class ThreadPool(object):
    def __init__(self, thread_num=8):
        self.page_num = 1
        self.pool_list = []
        self.thread_num = thread_num
        self.lock_page_num = threading.Lock()
        self.stop_flag = False
        self.lock_stop_flag = threading.Lock()
        self.lock_data_list = threading.Lock()
        self.data_list = []
        for i in range(self.thread_num):
            temp = threading.Thread(target=self.get_data_list)
            self.pool_list.append(temp)
        logging.debug("Thread pool is initialized...")

    def get_data_list(self):
        self.lock_page_num.acquire()
        try:
            cur_page = self.page_num
            self.page_num += 1
        finally:
            self.lock_page_num.release()
        content = net.open_url(cur_page)
        item_list = net.parse_content(content)
        if len(item_list) == 0:
            self.stop_flag = True
        self.lock_data_list.acquire()
        try:
            self.data_list.append(item_list)
        finally:
            self.lock_data_list.release()

    def start(self):
        for t in self.pool_list:
            t.start()

        while True:
            time.sleep(0.5)
            if not self.pool_list:
                logging.debug("Thread pool is empty...")
                break
            for t in self.pool_list:
                if not t.is_alive():
                    self.pool_list.remove(t)
                    self.lock_stop_flag.acquire()
                    try:
                        if not self.stop_flag:
                            temp = threading.Thread(target=self.get_data_list)
                            self.pool_list.append(temp)
                            temp.start()
                    finally:
                        self.lock_stop_flag.release()
