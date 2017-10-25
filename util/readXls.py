import xlrd

#读取Excel表格数据
def read_xls(filename="../write.xls"):
    data = xlrd.open_workbook(filename)
    name = data.sheets()[0]  # 通过索引顺序获取
    hometown = data.sheets()[1]  # 通过索引顺序获取
    dialect = data.sheets()[2]  # 通过索引顺序获取
    name = char_to_bit(name)
    hometown = char_to_bit(hometown)
    dialect = char_to_bit(dialect)
    return name,hometown,dialect

#对数据去除第一行和第一列的索引条目，得到纯粹的数据，并对y,n,m设值为1,0,0
def char_to_bit(table):
    nrows = table.nrows
    ncols = table.ncols
    result=[]
    for row in range(1,nrows):
        temp = table.row_values(row)[1:]
        rr=[]
        for i in range(0,len(temp)):
            if temp[i]=='n':
                rr.append(0)
            elif temp[i]=='y':
                rr.append(1)
            else:
                rr.append(0)
        result.append(rr)
    return result

#打印table
def printList(table):
    for row in table:
        print(row)