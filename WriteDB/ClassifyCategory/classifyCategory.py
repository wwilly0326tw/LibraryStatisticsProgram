import re
import sys
import time
import mysql.connector
import logging
import logging.config
import DBconfig as DBconfig
from time import gmtime, strftime

""" 將SFX中的主題分類建立與table Theme 的relation, 輸入sfxID將此ID建立分類關聯 或 將資料庫中未建立關聯的都跑過一遍  """

logging.config.fileConfig("../../logger.conf")
logger = logging.getLogger("root")

try:
    conn = mysql.connector.connect(user=DBconfig.user, password=DBconfig.password, database=DBconfig.database,
                                   host=DBconfig.host)
    cur = conn.cursor()
except Exception as err:
    logger.error(err)
    sys.exit(-1)

def classify(sfxID="", year=""):
    if year == "":
        year = strftime("%Y", gmtime())
    if sfxID is "":
        try:
            cur.execute("SELECT id, categories FROM sfx where year = " + str(year) + " and id not in (select sfxid from relation_sfx_theme )")
            sfxIDResult = cur.fetchall()
        except Exception as err:
            print (err)
            logger.error(err)
            sys.exit(-1)
    else:
        try:
            cur.execute("SELECT id, categories FROM sfx where id = " + str(sfxID))
            sfxIDResult = cur.fetchall()
        except Exception as err:
            logger.error(err)
            sys.exit(-1)

    try:
        cur.execute("SELECT tid, name from theme where year = " + str(year))
        themeResult = cur.fetchall()
    except Exception as err:
        logger.error(err)
        sys.exit(-1)

    for row in sfxIDResult:
        categoryStr = row[1]
        categoryList = []
        if categoryStr is None:
            continue
        print (categoryStr)
        for theme in themeResult:
            if categoryStr.find(theme[1]) is not -1:
                categoryList.append(theme[0])
        if categoryList:
            print (categoryList)
            insertRelStmt = "insert into relation_sfx_theme(sfxid, tid) values(" + str(row[0]) + ", "
            for ID in categoryList:
                try:
                    cur.execute(insertRelStmt + str(ID) + ")")
                    conn.commit()
                except Exception as err:
                    print(insertRelStmt + str(ID) + ")")
                    logger.error(err)
                    conn.rollback()
                    continue

    return

if __name__ == '__main__':
    logging.config.fileConfig("../../logger.conf")
    logger = logging.getLogger("root")
    classify(year="2018")
