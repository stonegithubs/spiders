letterList = ['ABCDEFGHI', 'JKLMNOPQR', 'STUVWXYZ*']
letterSubDict = {}


def comp_sub():
    global letterSubDict
    for i, j in enumerate(letterList):
        for a, b in enumerate(j):
            letterSubDict[b] = [i, a]


def encry():
    global letterSubDict
    date = input('输入日期:')
    dateList = [int(i) for i in date.split(' ')]
    strInfor = input('输入字符串:')
    strInfor = strInfor.replace(' ', '*')
    Mnums = (dateList[0] - 1) % 3
    Dnums = (dateList[1] - 1) % 9
    for i, j in letterSubDict.items():
        j[0] = str((3 + (j[0] - Mnums)) % 3 + 1)
        j[1] = str((9 + (j[1] - Dnums)) % 9 + 1)
        letterSubDict[i] = j
    position = []
    for i in strInfor:
        posit = ''.join(letterSubDict[i])
        position.append(posit)
    position = ' '.join(position)
    print(position)


if __name__ == '__main__':
    comp_sub()
    encry()
