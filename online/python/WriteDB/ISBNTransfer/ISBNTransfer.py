import re

def ISBN10to13(ISBN="9781509010660"):
    if ISBN is None:
        return ""
    if len(ISBN) < 10:
        return ""
    ISBN = str(ISBN)
    ISBN = re.sub("[^0-9Xx]", "", ISBN)
    if len(ISBN) > 12:
        return ISBN

    isbnVal1 = 9
    isbnVal2 = 21
    isbnVal3 = 8
    isbnVal4 = int(ISBN[0: 1]) * 3
    isbnVal5 = int(ISBN[1: 2]) * 1
    isbnVal6 = int(ISBN[2: 3]) * 3
    isbnVal7 = int(ISBN[3: 4]) * 1
    isbnVal8 = int(ISBN[4: 5]) * 3
    isbnVal9 = int(ISBN[5: 6]) * 1
    isbnVal10 = int(ISBN[6: 7]) * 3
    isbnVal11 = int(ISBN[7: 8]) * 1
    isbnVal12 = int(ISBN[8: 9]) * 3
    isbnSum = isbnVal1 + isbnVal2 + isbnVal3 + isbnVal4 + isbnVal5 + isbnVal6 + isbnVal7 + isbnVal8 + isbnVal9 \
              + isbnVal10 + isbnVal11 + isbnVal12
    isbnRemainder = isbnSum % 10
    isbnCheckSum = 10 - isbnRemainder
    if isbnCheckSum == 10:
        isbnCheckSum = 0
    isbn13 = "978" + ISBN[0:9] + str(isbnCheckSum)
    return isbn13
if '__main__' == __name__:
    ISBN10to13()
