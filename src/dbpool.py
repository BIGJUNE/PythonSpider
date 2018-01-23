import pymysql
import configparser
import logging
from DBUtils.PooledDB import PooledDB
__author__ = 'JackGao'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')


class DbPool(object):
    def __init__(self, mincon=4):
        # Initialize the database connection pool
        logging.debug('Begin to initialize the database connection pool...')
        config = configparser.ConfigParser()
        config.read('conf.ini')
        db_config = config['mysql']
        self.pool = PooledDB(pymysql, mincon, host=db_config['host'], user=db_config['user'], passwd=db_config['password'],
                             db=db_config['db'], port=3306, charset=db_config['charset'])
        logging.debug('Initialize the database connection pool(size=[%d]) success!' % mincon)

    def get_connect(self):
        return self.pool.connection()


# Define a singleton object
db_pool = DbPool(4)
