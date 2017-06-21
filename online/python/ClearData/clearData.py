import sys
import logging.config
import mysql.connector
import DBconfig as DBconfig

logging.config.fileConfig("../python/logger.conf")
logger = logging.getLogger("root")
toCommit = 1
# 比對結束清除資料(scopus、score)
try:
    conn = mysql.connector.connect(user=DBconfig.user, password=DBconfig.password, database=DBconfig.database,
                                   host=DBconfig.host)
    cur = conn.cursor()
except Exception as err:
    logger.error(err)
    sys.exit(-1)

def clearData():
    if checkThreadCount():
        return
    try:
        cur.execute("Update target set score = 0")
        if toCommit:
            conn.commit()
    except Exception as err:
        conn.rollback()
        logger.info('Zero score error.')
        logger.error(err)
    try:
        cur.execute("Delete from scopus where id > 0")
        if toCommit:
            conn.commit()
    except Exception as err:
        conn.rollback()
        logger.info('Delete Scopus error.')
        logger.error(err)
    return 1

def checkThreadCount():
    try:
        nThread = open('../python/flag', 'r')
        flag = int(nThread.read())
        return flag
    except Exception as err:
        logger.error(err)
        sys.exit(-1)
if __name__ == '__main__':
    clearData()
