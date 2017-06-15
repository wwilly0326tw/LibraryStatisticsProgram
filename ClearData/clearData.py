# 比對結束清除資料(scopus、score)
    # clearData()

def clearData():
    try:
        cur.execute("Update target set score = 0")
    except Exception as err:
        logger.info('Zero score error.')
        logger.error(err)
    try:
        cur.execute("Delete from ")
    except Exception as err:
        logger.info('Delete Scopus error.')
        logger.error(err)