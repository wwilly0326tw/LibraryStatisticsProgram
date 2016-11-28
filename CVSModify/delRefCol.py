# -*- coding:utf-8 -*-
f = open('testdata.txt', 'r', encoding='utf8')
rel = open('output.txt', 'w', encoding='utf8')

title = 1
for line in f:
    if title:
        rel.write(line)
        title = 0
        continue
    index = 0
    nCol = 0
    parsedLine = ""
    while index < len(line):
        if nCol is not 23:
            if line[index] is "\"":
                index2 = line.find('\",', index)
                parsedLine += line[index: index2 + 2]
                index = index2 + 2
                nCol += 1
            elif line[index] is ",":
                parsedLine += ","
                index += 1
                nCol += 1
            else:
                parsedLine += line[index]
                index += 1
        else:
            parsedLine += line[line.find("\",", index + 1) + 1: len(line)]
            break
    rel.write(parsedLine)