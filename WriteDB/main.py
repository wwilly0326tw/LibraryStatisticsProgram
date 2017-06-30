from WriteDB.writeSFXtoDB import writeSFX2DB
from ParseDate.parseDate import extractInterval
from ISBNTransfer.ISBNTransfer import ISBN10to13
from WriteDB.writeDepartment import writeDepartment
from WriteDB.relateSFXDepart import relate_SFX_Depart
from WriteDB.relateThemeDepart import relate_Theme_Department
from WriteDB.ClassifyCategory.classifyCategory import classify

import sys
from time import gmtime, strftime
import logging
import logging.config
import mysql.connector
import DBconfig as DBconfig


""" 建置資料流程 """
logging.config.fileConfig("../logger.conf")
logger = logging.getLogger("root")
toCommit = 1
debug = 1

try:
    conn = mysql.connector.connect(user=DBconfig.user, password=DBconfig.password, database=DBconfig.database,
                                   host=DBconfig.host)
    cur = conn.cursor()
except Exception as err:
    logger.error(err)
    sys.exit(-1)

def main(sfxFileName="", themeFileName="", departFileName="", year=""):
    if sfxFileName == "":
        return
    if len(sys.argv) > 1:
        sfxFileName = sys.argv[1]
        if len(sys.argv) > 2:
            themeFileName = sys.argv[2]
            if len(sys.argv) > 3:
                departFileName = sys.argv[3]
    if year == "":
        year = strftime("%Y", gmtime())
    # 先將每次的sfx寫入DB(程式給定年分) writeSFXtoDB
    if sfxFileName is not "" and not None:
        writeSFX2DB(sfxFileName, year)

    # 將sfx的Threshold轉成結構化的資料 parseDate
    try:
        cur.execute("SELECT id, Threshold from sfx where year = " + year)
        resultOfSFX = cur.fetchall()
        for row in resultOfSFX:
            parsedInterval = extractInterval(row[1])
            if parsedInterval is not "":
                try:
                    stmt = "UPDATE sfx set Threshold = '" + parsedInterval + "' where id = " + str(row[0])
                    if debug:
                        print (stmt)
                    cur.execute(stmt)
                    if toCommit:
                        conn.commit()
                except Exception as err:
                    conn.rollback()
                    logger.info('Update Threshold error.')
                    logger.error(err)
                    continue
    except Exception as err:
        logger.info('Get Threshold error.')
        logger.error(err)
        return

    # 將sfx的ISBN都轉成13碼
    try:
        cur.execute("SELECT id, ISBN, eISBN from sfx where year = " + year)
        resultOfSFX = cur.fetchall()
        for row in resultOfSFX:
            ISBN = ISBN10to13(row[1])
            eISBN = ISBN10to13(row[2])
            try:
                stmt = "UPDATE sfx set ISBN = '" + ISBN + "', eISBN = '" + eISBN + "' where id = " + str(row[0])
                if debug:
                    print (stmt)
                cur.execute(stmt)
                if toCommit:
                    conn.commit()
            except Exception as err:
                conn.rollback()
                logger.info('Update ISBN error.')
                logger.error(err)
                continue
    except Exception as err:
        logger.info('Get ISBN error.')
        logger.error(err)
        return

    # 建立Theme與Depart的relation relate_Theme_Depart
    if themeFileName is not "" and not None:
        relate_Theme_Department(themeFileName, year)

    # 將sfx分類至各theme(須給年分，預設處理今年) classifyCategory
    classify(year=year)

    # 更新SFX與Department的relation(須給年分，預設空值) relateSFXDepart
    relate_SFX_Depart(year=year)
if __name__ == '__main__':
    main(sfxFileName="../../Data/SFX/sfx2016.xlsx", themeFileName="../../Data/SFX/1051219sfx主題分類-學院系所對照.xlsx", year="2018")
    # main(sfxFileName="../../Data/SFX/20170421SFX_adv_both_both.xlsx", themeFileName="..\..\Data\SFX\\1051219sfx主題分類-學院系所對照.xlsx")