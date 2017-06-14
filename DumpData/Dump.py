from openpyxl import load_workbook
import mysql.connector
import DBconfig as DBconfig


def dump():
    wb = load_workbook(filename="scopus.xlsx")
    ws = wb[wb.sheetnames[0]]
    return
if __name__ == '__main__':
    # main(filename="../Data/scopus/scopus.xlsx")
    dump()