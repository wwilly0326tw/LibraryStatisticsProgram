import Program.DBconfig as DBconfig
import mysql.connector
import logging
import logging.config

""" 程式用途為更新sfx to dep 的relation """

def relate_SFX_Depart(year = ""):
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
        cur.execute("insert relation_sfx_department select a.id as sfxid, c.did as did from sfx a, relation_sfx_theme b,"
                    " relation_theme_department c, department d where a.year = " + str(year) + " a.id = b.sfxid and b.tid = c.tid and c.did = d.did group by did, id")
        conn.commit()
    except Exception as err:
        logger.error(err)
        conn.rollback()

if __name__ == '__main__':
    relate_SFX_Depart()