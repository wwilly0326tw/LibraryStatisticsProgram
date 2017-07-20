# -*-coding: utf-8-*-
from ISBNTransfer.ISBNTransfer import ISBN10to13
import sys
import time
import DBconfig as DBconfig
import mysql.connector
import logging
import logging.config

"""Input ISSN 或 ISBN 數組，比較相同的SFX資料回傳"""
debug = 0

def cmpISSNISBN(ISSN="", ISBN="", year=""):
    logger = logging.getLogger("root")
    try:
        conn = mysql.connector.connect(user=DBconfig.user, password=DBconfig.password, database=DBconfig.database,
                                       host=DBconfig.host)
        cur = conn.cursor()
    except Exception as err:
        logger.error(err)
        return False

    if ISSN is not "":
        ISSNstr = ISSN
        if ISSN.find(";") is not -1:
            ISSNstr = split(ISSN=ISSN)
        try:
            stmt = "SELECT ID FROM (SELECT id, year, ISSN, eISSN from sfx where " \
                   "ISSN in ('" + ISSNstr + "') or eISSN in ('" + ISSNstr + "')) AS A WHERE A.year = " + str(year)
            if debug:
                print (stmt)
            cur.execute(stmt)
            return cur.fetchall()
        except Exception as err:
            logger.error(err)
            return None
    elif ISBN is not "":
        ISBNstr = ISBN
        if ISBN.find(";") is not -1:
            ISBNstr = split(ISBN=ISBN)
        try:
            stmt = "SELECT ID FROM (SELECT id, year, ISSN, eISSN from sfx where " \
                   "ISBN in ('" + ISBNstr + "') or eISBN in ('" + ISBNstr + "')) AS A WHERE A.year = " + str(year)
            if debug:
                print(stmt)
            cur.execute(stmt)
            return cur.fetchall()
        except Exception as err:
            logger.error(err)
            return None
    else:
        return None

def split(ISSN="", ISBN=""):
    retStr = ""
    if ISSN is not "":
        array = ISSN.split(";")
        for row in array:
            retStr += row
            retStr += "','"
        return retStr[0:-3]
    elif ISBN is not "":
        array = ISBN.split(";")
        for row in array:
            retStr += ISBN10to13(row)
            retStr += "','"
        return retStr[0:-3]
    else:
        return

def traceback(err):
    now = time.strftime('%H:%M:%S', time.localtime(time.time()))
    tb = sys.exc_info()[2]
    print(now, err, 'exception in line', tb.tb_lineno)


if __name__ == '__main__':
    logging.config.fileConfig("../logger.conf")
    logger = logging.getLogger("root")
    cmpISSNISBN(ISSN="00189340", year="2016")