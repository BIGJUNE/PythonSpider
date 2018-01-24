# -*- coding:utf-8 -*-
import threading
from src import net, dbpool
import time
import logging
__author__ = 'JackGao'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')


class ThreadPool(object):
    def __init__(self, thread_num=2):
        self.page_num = 0
        self.tag_num = 0
        self.pool_list = []
        self.thread_num = thread_num
        self.stop_flag = False
        self.data_list = []
        self.data_size = 0
        self.cookie = ''
        for i in range(self.thread_num):
            temp = threading.Thread(target=self.get_data_list)
            self.pool_list.append(temp)
        logging.debug("Thread pool is initialized...")
        # lock
        self.lock_list = threading.Lock()

    def get_data_list(self):
        cur_page = self.page_num
        cur_tag = self.tag_num
        self.page_num += 1
        r = net.open_url(cur_tag, cur_page, self.cookie)

        if r.status_code != 200:
            if not self.cookie:
                raise RuntimeError("访问被禁止!!!")
            else:
                self.cookie = ''
        else:
            if not self.cookie:
                self.cookie = r.cookies['bid']
            item_list = net.parse_content(r.text)
            if len(item_list) == 0:
                if cur_page == 0:
                    self.stop_flag = False
                else:
                    self.tag_num = cur_tag + 1
                    self.page_num = 0
            else:
                self.data_size += len(item_list)
                logging.debug("The program has collected %d data" % self.data_size)
                self.lock_list.acquire()
                try:
                    for i in item_list:
                        self.data_list.append(i)
                finally:
                    self.lock_list.release()

    def start(self):
        for t in self.pool_list:
            t.start()

        while True:
            time.sleep(2)
            if not self.pool_list:
                logging.debug("Thread pool is empty...")
                break
            for t in self.pool_list:
                if not t.is_alive():
                    self.pool_list.remove(t)
                    if not self.stop_flag:
                        temp = threading.Thread(target=self.get_data_list)
                        self.pool_list.append(temp)
                        temp.start()
