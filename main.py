from Program.CmpISSN.ISSN_Comp import cmpISSN
from Program.CmpInterval.cmpInterval import cmpInterval
from openpyxl import load_workbook
from termcolor.termcolor import colored
import logging
import logging.config
import sys
import re
import Program.DBconfig as DBconfig
import mysql.connector

"""此程式用於統合比對ISSN以及年卷期，回傳是否有購買此篇參考文獻"""
logging.config.fileConfig("./logger.conf")
logger = logging.getLogger("root")
try:
    conn = mysql.connector.connect(user=DBconfig.user, password=DBconfig.password, database=DBconfig.database,
                                   host=DBconfig.host)
    cur = conn.cursor()
except Exception as err:
    logger.error(err)
    sys.exit(-1)


def main(filename="testdata.xlsx"):
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    if filename is not "":
        wb = load_workbook(filename=filename, read_only=True)
        ws = wb[wb.sheetnames[0]]
        dataStr = 'A30035:J' + str(ws.max_row)
        for row in ws[dataStr]:
            sfxIDList = cmpISSN(row[8].value) # 比對到ISSN的清單
            scopusID = insertDB(row) # 將scopus的資料insert到DB
            if sfxIDList is not None and len(sfxIDList) is not 0:
                try:
                    cur.execute("SELECT year, volume, issue from scopus where id = " + str(scopusID))
                    YVI = cur.fetchone()
                except Exception as err:
                    logger.info('Select YVI from scopus error.')
                    logger.error(err)
                    continue
                for sfxID in sfxIDList:
                    try:
                        cur.execute("SELECT Threshold from sfx where id=" + str(sfxID[0]))
                        threshold = cur.fetchone()[0]
                    except Exception as err:
                        logger.info('Select threshold from sfx error.')
                        logger.error(err)
                        continue
                    if cmpInterval(threshold, str(YVI[0]) + "." + str(YVI[1]) + "." + str(YVI[2])):
                        try:
                            cur.execute("INSERT INTO support(sfxID, scopusID) values(" + str(sfxID[0]) + "," + str(scopusID) + ")")
                            conn.commit()
                        except Exception as err:
                            logger.info('Create relation in support error.')
                            logger.error(err)
                            continue
                    else:
                        print (threshold)
                        print (YVI)
                        print(colored('Interval not match.', 'red'))
            else:
                print(row[8].value)
                print(colored('ISSN not match.', 'red'))

    else:
        print('Please Input the File.')
        return


def insertDB(row):
    sqlStmt = "INSERT INTO scopus(author_keyword, book_name, year, source_name, volume, issue, DOI, link, ISSN, ISBN) values("
    valStr = ""
    for col in row:
        if col.value is None:
            valStr += 'NULL'
        else:
            valStr += "\""
            valStr += str(col.value).replace("\"", "'").replace("\\", "")
            valStr += "\""
        valStr += ", "
    valStr = valStr[0: len(valStr) - 2]
    valStr += ")"
    try:
        cur.execute(sqlStmt + valStr)
        conn.commit()
        # 修改卷期非數字的問題
        scoupusID = cur.lastrowid
    except Exception as err:
        print(sqlStmt + valStr)
        logger.error(err)
        conn.rollback()
        return
    modifyYVI(scoupusID)
    return scoupusID


def modifyYVI(scoupusID):
    try:
        cur.execute("SELECT year, volume, issue from scopus where id = " + str(scoupusID))
        result = cur.fetchone()
    except Exception as err:
        logger.info("Select YVI to modify error.")
        logger.error(err)
        return False
    updateFlag = 0
    tmpList = [result[0], result[1], result[2]]
    if result[0] is None or not re.match('^[0-9]+$', result[0]):
        tmpList[0] = 0
        updateFlag = 1
    if result[1] is None or not re.match('^[0-9]+$', result[1]):
        tmpList[1] = 0
        updateFlag = 1
    if result[2] is None or not re.match('^[0-9]+$', result[2]):
        tmpList[2] = 0
        updateFlag = 1
    if updateFlag:
        try:
            cur.execute("UPDATE scopus set year=" + str(tmpList[0]) + ",volume=" + str(tmpList[1]) + ", issue=" + str(tmpList[2]) + " where id = " + str(scoupusID))
            conn.commit()
        except Exception as err:
            logger.info('Update YVI error.')
            logger.error(err)
            return False

if __name__ == '__main__':
    main(filename="../Data/scopus/scopus.xlsx")
    # main()