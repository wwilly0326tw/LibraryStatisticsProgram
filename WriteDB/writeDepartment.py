import Program.DBconfig as DBconfig
import mysql.connector
import logging
import logging.config


""" 程式用途為更新Department Table """
""" 查資料庫中存不存在，不存在就往後加上去，要對應到院 """

def writeDepartment(filename = ""):
    if filename == "":
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

if __name__ == '__main__':
    writeDepartment()