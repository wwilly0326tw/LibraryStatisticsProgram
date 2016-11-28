# -*-coding: <utf-8-*-
import sys
import time
from termcolor.termcolor import colored
from openpyxl import Workbook
from openpyxl import load_workbook

PISSN = []
EISSN = []

"""從sfx中取出PISSN EISSN"""


def getISSN():
    print(colored('Reading SFX-ISSN...', 'blue', attrs=['bold', 'underline']))
    wb = load_workbook(filename='./Data/sfxISSN.xlsx', read_only=True)
    # wb = load_workbook(filename = 'test.xlsx', read_only=True)
    ws = wb[wb.sheetnames[0]]

    PISSN_str = 'A1:A' + str(ws.max_row)
    EISSN_str = 'B1:B' + str(ws.max_row)

    for row in ws[PISSN_str]:
        # print (cell.value)
        PISSN.append(row[0].value)
    for row in ws[EISSN_str]:
        # print (cell.value)
        EISSN.append(row[0].value)
    print(colored('Reading SFX-ISSN... ', 'blue', attrs=['bold', 'underline']) + colored('Completed.', 'yellow'))

"""比對PISSN EISSN 是否有相同的，若相同回傳其index"""


def cmpISSN(ISSN):
    index = -1
    try:
        index = EISSN.index(ISSN)
    except ValueError:
        try:
            index = PISSN.index(ISSN)
        except ValueError:
            index = -1

    if index is not -1:
        print (colored('Match ISSN in index :  ', 'blue', attrs=['bold', 'underline']) + colored(str(index), 'yellow'))
        return index


# def cmpISSN():
#     count = 0
#     totalRowIndex = 1
#     startTime = time.time()
#
#     """This output is Matched the ISSN"""
#     outputwb = Workbook()
#     outputws = outputwb[outputwb.sheetnames[0]]
#     outputData = []
#     outputws.append(header)
#     outputwb.save('./resultData/MatchISSN.xlsx')
#
#     """This output is Not Matched the ISSN"""
#     outputwb2 = Workbook()
#     outputws2 = outputwb2[outputwb2.sheetnames[0]]
#     outputData2 = []
#     outputws2.append(header)
#     outputwb2.save('./resultData/noMatchISSN.xlsx')
#
#     for year in range(2016, 2017):
#         print('Processing ' + str(year) + " year's file.")
#         wb = load_workbook(filename='Data/Year/' + str(year) + '.xlsx', read_only=True)
#         ws = wb[wb.sheetnames[0]]
#         rowIndex = 1
#         ISSN_str = 'Q2:Q' + str(ws.max_row)
#
#         for row in ws[ISSN_str]:
#             totalRowIndex += 1
#             rowIndex += 1
#             if row[0].value is None:
#                 continue
#             if totalRowIndex % 1000 is 0:
#                 print('Total processed count : ' + str(totalRowIndex))
#                 endTime = time.time()
#                 print('Time consuming : ' + str(endTime - startTime))
#                 startTime = time.time()
#
#             elif row[0].value in PISSN or row[0].value in EISSN:
#                 count += 1
#
#                 for one_row in ws.iter_rows(str(rowIndex)):
#                     for col in one_row:
#                         outputData.append(col.value)
#                 nRow = outputws.max_row + 1
#                 for i in range(1, len(outputData) + 1):
#                     outputws.cell(row=nRow, column=i).value = outputData[i - 1]
#                 outputData = []
#
#             else:
#                 for one_row in ws.iter_rows(str(rowIndex)):
#                     for col in one_row:
#                         outputData2.append(col.value)
#                 nRow = outputws2.max_row + 1
#                 for i in range(1, len(outputData2) + 1):
#                     outputws2.cell(row=nRow, column=i).value = outputData2[i - 1]
#                 outputData2 = []
#
#         print('Match count : ' + str(count))
#         print('Saving files.')
#         outputwb.save('./resultData/MatchISSN.xlsx')
#         outputwb2.save('./resultData/noMatchISSN.xlsx')


def traceback(err):
    now = time.strftime('%H:%M:%S', time.localtime(time.time()))
    tb = sys.exc_info()[2]
    print(now, err, 'exception in line', tb.tb_lineno)


if __name__ == '__main__':
    print (cmpISSN('0033-1236'))
