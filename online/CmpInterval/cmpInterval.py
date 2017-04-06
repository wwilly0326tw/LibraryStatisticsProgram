import re

"""輸入必須先將refInterval弄成x.x.x格式"""


def cmpInterval(parsedInterval, refInterval):
    if parsedInterval is None:
        return True
    refInterval = re.split('\.', refInterval)
    for cell in re.split(' ', parsedInterval):
        # print(cell)
        if cell.find('-') is not -1:
            start = cell[0: cell.find('-')]
            start = re.split('\.', start)
            # print(start)
            end = cell[cell.find('-') + 1: len(cell)]
            end = re.split('\.', end)
            # print(end)
            if start[0] <= refInterval[0] <= end[0] or refInterval[0] is 0:
                if start[1] <= refInterval[1] <= end[1] or refInterval[1] is 0:
                    if start[2] <= refInterval[2] <= end[2] or refInterval[2] is 0:
                        # print (cell)
                        return True
        elif cell.find('.') is not -1: # 比對Available in 的寫法
            start = re.split('\.', cell)
            if start[1] is 0:
                start[1] = refInterval[1]
            if start[2] is 0:
                start[2] = refInterval[2]
            if start[0] is refInterval[0] and start[1] is refInterval[1] and start[2] is refInterval[2]:
                # print(cell)
                return True
    return False

if __name__ == '__main__':
    buyInter = "2007.24.1 2007.24.3-2007.24.5 2015.32.2 2015.32.4-2015.32.6"
    ref = "2015.32.6"
    if cmpInterval(buyInter, ref):
        print("Match")
    else:
        print("Nmatch")