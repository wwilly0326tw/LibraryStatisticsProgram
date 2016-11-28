import re
import time

"""處理給予的檔案或是字串，回傳結構化的區間資料(input string) 或輸出成result.txt(input file)"""


def extractInterval(string="", filename=""):
    f = ""
    if filename is not "":
        f = open(filename, 'r')
    rel = open('result.txt', 'w')
    if f:
        for line in f:
            """處理 parseDate 字串"""
            parsedData = []
            print(line)
            for cell in re.split('\. ', line):
                # print(cell)
                if cell.find('Available') is not -1:
                    parsedData.append(parseYVI(cell))
                if cell.find('Most') is not -1:
                    recent = parseRecent(parsedData, cell)
                    rowIndex = 0
                    for row in parsedData:
                        if row[row.find('-') + 1: row.find('-') + 2] is '9':
                            parsedData[rowIndex] = row[0: row.find('-') + 1] + recent + row[row.find('-') + 5: len(row)]
                            break
                        rowIndex += 1
            print(parsedData)
            for str in parsedData:
                rel.write(str)
                rel.write(' ')
            rel.write('\n')
    elif string:
        """處理 parseDate 字串"""
        parsedData = []
        # print(string)
        for cell in re.split('\. ', string):
            # print(cell)
            if cell.find('Available') is not -1:
                parsedData.append(parseYVI(cell))
            if cell.find('Most') is not -1:
                recent = parseRecent(parsedData, cell)
                rowIndex = 0
                for row in parsedData:
                    if row[row.find('-') + 1: row.find('-') + 2] is '9':
                        parsedData[rowIndex] = row[0: row.find('-') + 1] + recent + row[row.find('-') + 5: len(row)]
                        break
                    rowIndex += 1
        # print(parsedData)
        retStr = ""
        for str in parsedData:
            rel.write(str)
            rel.write(' ')
            retStr += str
            retStr += ' '
        rel.write('\n')
        return retStr


"""用來處理年卷期的功能"""


def parseYVI(cell):
    cell += ' '
    parsedCell = ""
    start = cell.find(' ', cell.find(' ') + 1) + 1
    if start is not -1:
        parsedCell += cell[start: start + 4]
        pos = cell.find('volume')
        if pos is not -1:
            parsedCell += "."
            parsedCell += cell[pos + 8: cell.find(' ', pos + 8)]
        else:
            parsedCell += "."
            parsedCell += "0"
        pos = cell.find('issue')
        if pos is not -1:
            parsedCell += "."
            parsedCell += cell[pos + 7: cell.find(' ', pos + 7)]
        else:
            parsedCell += "."
            parsedCell += "0"

    end = cell.find('until')
    if end is not -1:
        parsedCell += "-"
        parsedCell += cell[end + 6: end + 10]
        pos = cell.find('volume', end)
        if pos is not -1:
            parsedCell += "."
            parsedCell += cell[pos + 8: cell.find(' ', pos + 8)]
        else:
            parsedCell += "."
            parsedCell += "9999"
        pos = cell.find('issue', end)
        if pos is not -1:
            parsedCell += "."
            print(cell[pos + 6])
            parsedCell += cell[pos + 7: len(cell) - 1]
        else:
            parsedCell += "."
            parsedCell += "9999"
    elif cell.find('from') is not -1:
        parsedCell += "-9999.9999.9999"
    return parsedCell


"""擷取近幾年幾個月不能瀏覽"""


def parseRecent(parsedData, cell):
    parsedCell = ""
    start = cell.find('nt ')
    parsedCell += cell[start + 3: cell.find(' ', start + 3)]
    year = 0
    month = 0
    if cell.find('year') is not -1:
        year = int(parsedCell)
        if cell.find('month') is not -1:
            start = cell.find('year')
            month = int(cell[start + 8: cell.find(' ', start + 8)])
    else:
        month = int(parsedCell)

    recent = int(time.strftime("%Y")) - year - int((month / 12))
    if month % 12 and int(time.strftime("%m")) - (month % 12) < 0:
        recent -= 1
    return str(recent)


if __name__ == '__main__':
    print(extractInterval(filename='testdata.txt'))
