import DBconfig as DBconfig
import mysql.connector
import sys

"""程式用途： 取資料庫中Support(1)、Theme(2)、Department(3)、College(4) View的資料"""

debug = 1

def getView(view=0, batchID=0):
    if sys.argv[1]:
        view = sys.argv[1]
    if sys.argv[2]:
        batchID = sys.argv[2]
    try:
        filename = ""
        if view == "2":
            filename = "支援主題排序表(" + str(batchID) + ").txt"
        elif view == "3":
            filename = "支援科系排序表(" + str(batchID) + ").txt"
        elif view == "4":
            filename = "支援院別排序表(" + str(batchID) + ").txt"
        outputFile = open("../result/" + filename, 'w+', encoding='UTF-8')
    except Exception as err:
        print (err)
        sys.exit(-1)

    try:
        conn = mysql.connector.connect(user=DBconfig.user, password=DBconfig.password, database=DBconfig.database,
                                       host=DBconfig.host)
        cur = conn.cursor()
    except Exception as err:
        if debug:
            print (err)
    if view == "1":
        cur.execute("select * from `v_journal_support(all)` where batchID = " + str(batchID))
        result = cur.fetchall()
    elif view == "2":
        outputFile.write("Count")
        outputFile.write('\t')
        outputFile.write("Theme")
        outputFile.write('\n')
        cur.execute("select count, name from `v_journal_support_theme_rank(all)` where batchID = " + str(batchID) + " order by count desc")
        result = cur.fetchall()

    elif view == "3":
        outputFile.write("Count")
        outputFile.write('\t')
        outputFile.write("Theme")
        outputFile.write('\n')
        cur.execute("select count, name from `v_journal_support_department_rank(all_usesfxtodep)` where batchID = " + str(batchID) + " order by count desc")
        result = cur.fetchall()

    elif view == "4":
        outputFile.write("Count")
        outputFile.write('\t')
        outputFile.write("Theme")
        outputFile.write('\n')
        cur.execute("select count, name from `v_journal_support_college_rank(all)` where batchID = " + str(batchID) + " order by count desc")
        result = cur.fetchall()

    else:
        if debug:
            print ("Error View Type.")
        return

    for row in result:
        for col in row:
            outputFile.write(str(col))
            outputFile.write('\t')
        outputFile.write('\n')
    print (filename)
    outputFile.close()

if __name__ == '__main__':
    getView(str(1), str(2))