from Program.WriteDB.writeSFXtoDB import writeSFX2DB
from Program.ParseDate.parseDate import extractInterval
from Program.WriteDB.writeDepartment import writeDepartment
from Program.WriteDB.relateSFXDepart import relate_SFX_Depart
from Program.WriteDB.relateThemeDepart import relate_Theme_Department
from Program.WriteDB.ClassifyCategory.classifyCategory import classify
import sys
import time
import logging
import logging.config
import mysql.connector
import Program.DBconfig as DBconfig


""" 建置資料流程 """
logging.config.fileConfig("../logger.conf")
logger = logging.getLogger("root")
toCommit = True
debug = 1

try:
    conn = mysql.connector.connect(user=DBconfig.user, password=DBconfig.password, database=DBconfig.database,
                                   host=DBconfig.host)
    cur = conn.cursor()
except Exception as err:
    logger.error(err)
    sys.exit(-1)

def main(sfxFileName="", themeFileName="", departFileName=""):
    if sfxFileName == "":
        return
    if len(sys.argv) > 1:
        sfxFileName = sys.argv[1]
        if len(sys.argv) > 2:
            themeFileName = sys.argv[2]
            if len(sys.argv) > 3:
                departFileName = sys.argv[3]
    # 先將每次的sfx寫入DB(DB自動帶入今年年分) writeSFXtoDB
    if sfxFileName is not "" and not None:
        writeSFX2DB(sfxFileName)
    # 將sfx的Threshold轉成結構化的資料 parseDate
    try:
        cur.execute("SELECT id, Threshold from sfx where year in (select year(now()) as year)")
        resultOfSFX = cur.fetchall()
        for row in resultOfSFX:
            parsedInterval = extractInterval(row[1])
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
    # 若要更新Department(寫入未在table內的) writeDepartment (此程式尚未完成)
    # if departFileName is not "" and not None:
    #     writeDepartment(departFileName)
    # 建立Theme與Depart的relation(自動帶入今年年分) relate_Theme_Depart
    if themeFileName is not "" and not None:
        relate_Theme_Department(themeFileName)
    # 將sfx分類至各theme(須給年分，預設處理今年) classifyCategory
    classify()
    # 更新SFX與Department的relation(須給年分，預設空值) relateSFXDepart
    relate_SFX_Depart(time.strftime("%Y"))
if __name__ == '__main__':
    # main(sfxFileName="../Data/SFX/20170421SFX_adv_both_both.xlsx")
    main(sfxFileName="../testdata.xlsx",themeFileName="..\..\Data\SFX\\1051219sfx主題分類-學院系所對照.xlsx")