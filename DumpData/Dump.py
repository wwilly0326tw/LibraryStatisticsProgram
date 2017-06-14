from openpyxl import load_workbook
import mysql.connector
import DBconfig as DBconfig

conn = mysql.connector.connect(user=DBconfig.user, password=DBconfig.password, database=DBconfig.database,
                               host=DBconfig.host)
cur = conn.cursor()


def dump():
    wb = load_workbook(filename="1.xlsx")
    ws = wb[wb.sheetnames[0]]
    dataStr = 'A2:A' + str(ws.max_row)
    for row in ws[dataStr]:
        scopusID = row[0].value
        cur.execute("Select sfxID from support where scopusID = " + str(scopusID))
        sfxIDList = cur.fetchall()
        if sfxIDList is not None and len(sfxIDList) is not 0:
            for id in sfxIDList:
                print (id)
    return
if __name__ == '__main__':
    # main(filename="../Data/scopus/scopus.xlsx")
    dump()