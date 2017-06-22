import Program.DBconfig as DBconfig
import mysql.connector
import logging
import logging.config
import sys

ifCommit = 0

""" 程式功能為刪除某一年相關的所有資料(sfx、theme、rel_theme_dep、rel_sfx_theme、rel_sfx_dep、support) """

def deleteData(year = ""):
    if len(sys.argv) > 1:
        year = sys.argv[1]
    if year == "":
        return False
    logging.config.fileConfig("../logger.conf")
    logger = logging.getLogger("root")
    try:
        conn = mysql.connector.connect(user=DBconfig.user, password=DBconfig.password, database=DBconfig.database,
                                       host=DBconfig.host)
        cur = conn.cursor()
    except Exception as err:
        logger.error(err)
        return False

    try:
        cur.execute("delete from sfx where year = " + str(year))
        cur.execute("delete from theme where year = " + str(year))
        if ifCommit:
            conn.commit()
    except Exception as err:
        logger.error(err)
        conn.rollback()

if __name__ == '__main__':
    deleteData()