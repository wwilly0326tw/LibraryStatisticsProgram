import DBconfig as DBconfig
import mysql.connector
import sys

"""程式用途： 取資料庫中Support(1)、Theme(2)、Department(3)、College(4) View的資料"""

debug = 1

def getView(view=0, batchID=0, year=""):
    if sys.argv[1]:
        view = sys.argv[1]
    if sys.argv[2]:
        batchID = sys.argv[2]
    if sys.argv[3]:
        year = sys.argv[3]
    try:
        filename = ""
        if view == "1":
            filename = "支援主題排序表(" + str(batchID) + ").txt"
        elif view == "2":
            filename = "支援科系排序表(" + str(batchID) + ").txt"
        elif view == "3":
            filename = "支援院別排序表(" + str(batchID) + ").txt"
        elif view == "4":
            filename = "支援資料庫排序表(" + str(batchID) + ").txt"
        elif view == "5":
            filename = "支援資料庫排序表(" + str(batchID) + "-Score).txt"
        elif view == "6":
            filename = "NMatchThemes.txt"
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
        outputFile.write("Theme")
        outputFile.write('\t')
        outputFile.write("Count")
        outputFile.write('\n')
        cur.execute("select name, count from `v_journal_support_theme_rank(all)` where batchID = " + str(batchID) + " order by count desc")
        result = cur.fetchall()

    elif view == "2":
        outputFile.write("Department")
        outputFile.write('\t')
        outputFile.write("Count")
        outputFile.write('\n')
        cur.execute("select name, count from `v_journal_support_department_rank(all_usesfxtodep)` where batchID = " + str(batchID) + " order by count desc")
        result = cur.fetchall()

    elif view == "3":
        outputFile.write("College")
        outputFile.write('\t')
        outputFile.write("Count")
        outputFile.write('\n')
        cur.execute("select name, count from `v_journal_support_college_rank(all_sfxtodep)` where batchID = " + str(batchID) + " order by count desc")
        result = cur.fetchall()

    elif view == "4":
        outputFile.write("Target")
        outputFile.write('\t')
        outputFile.write("Count")
        outputFile.write('\n')
        cur.execute("select name, count from `v_journal_support_target_rank(all)` where batchID = " + str(batchID) + " order by count desc")
        result = cur.fetchall()
    elif view == "5":
        outputFile.write("Target")
        outputFile.write('\t')
        outputFile.write("Score")
        outputFile.write('\n')
        cur.execute("select name, score from `v_journal_support_target_rank(all_score)`")
        result = cur.fetchall()
    elif view == "6":
        outputFile.write("Theme")
        outputFile.write('\n')
        cur.execute("select name from `v_nmatchtheme(all)` where year = " + str(year))
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