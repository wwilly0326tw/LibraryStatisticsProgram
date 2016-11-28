from ParseDate import parseDate
from CmpISSN import ISSN_Comp
from CmpInterval import cmpInterval
from openpyxl import load_workbook
from termcolor.termcolor import colored
import sys

"""此程式用於統合比對ISSN以及年卷期，回傳是否有購買此篇參考文獻"""


def main(filename="testdata.xlsx"):
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    if filename is not "":
        wb = load_workbook(filename=filename, read_only=True)
        ws = wb[wb.sheetnames[0]]
        ISSN_Comp.getISSN()
        ISSN_str = 'Q2:Q' + str(ws.max_row)
        refIndex = 0

        while refIndex < len(ws[ISSN_str]):
            index = ISSN_Comp.cmpISSN(ws[ISSN_str][refIndex][0].value)
            if index is not -1:
                sfxWB = load_workbook(filename='./Data/SFX/sfx.xlsx', read_only=True)
                sfxWS = sfxWB[wb.sheetnames[0]]
                parsedDate = parseDate.extractInterval(sfxWS['G' + str(index + 1)].value)
                rowYVI = ws['D' + str(refIndex + 2)].value + '.' + ws['F' + str(refIndex + 2)].value + '.' + ws[
                    'G' + str(refIndex + 2)].value
                print(colored('SFX interval:  ', 'blue', attrs=['bold', 'underline']) + colored(parsedDate, 'yellow'))
                print(colored('Ref YVI:  ', 'blue', attrs=['bold', 'underline']) + colored(rowYVI, 'yellow'))
                if cmpInterval.cmpInterval(parsedDate, rowYVI):
                    print(colored('Match', 'yellow'))
                    # extract YVI by index(SFX index)
                    # put it in the parseDate
                    # extract YVI from this row
                    # if(cmpInterval(parseDate, rowYVI))
                    # return match
            else:
                print(colored('ISSN not match.', 'red'))
            refIndex += 1


    else:
        print('Please Input the File Name.')
        return


if __name__ == '__main__':
    main()
