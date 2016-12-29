import re
import sys
import time
import mysql.connector
import logging
import logging.config
import Program.DBconfig as DBconfig

"""處理給予的檔案或是字串，回傳結構化的區間資料(input string) 或輸出成result.txt(input file)"""


def classify(string=""):
    try:
        conn = mysql.connector.connect(user=DBconfig.user, password=DBconfig.password, database=DBconfig.database,
                                       host=DBconfig.host)
        cur = conn.cursor()
        cur.execute("SELECT sid, name from subject")
        result = cur.fetchall()
    except Exception as err:
        logger.error(err)
        sys.exit(-1)
    retList = []
    for row in result:
        if string.find(row[1]) is not -1:
            retList.append(row[0])
    return retList

if __name__ == '__main__':
    logging.config.fileConfig("../logger.conf")
    logger = logging.getLogger("root")

    try:
        conn = mysql.connector.connect(user=DBconfig.user, password=DBconfig.password, database=DBconfig.database,
                                       host=DBconfig.host)
        cur = conn.cursor()
        cur.execute("SELECT id, category FROM sfx where id not in (select sfxid from category)")
        result = cur.fetchall()
    except Exception as err:
        logger.error(err)
        sys.exit(-1)

    for row in result:
        subjectList = classify(row[1])
        for sid in subjectList:
            try:
                cur.execute("INSERT into classify(sfxid, did) values(" + str(row[0]) + ", " + str(sid))
                conn.commit()
            except Exception as err:
                conn.rollback()
                logger.error(err)
                continue
