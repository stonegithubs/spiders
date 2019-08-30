# coding=utf-8

"""
1. 统计如下 list 单词及其出现次数,
    a_list = ['apple', 'banana', 'apple', 'tomato', 'orange', 'apple', 'banana', 'watermeton']

2. 请写出一段Python代码实现删除一个list里面的重复元素，不能使用set
    alist = [{"name":"a", "age":20}, {"name":"b", "age":30}, {"name":"c", "age":25}]


3. 用python编写一个函数,将以下文本格式，
        姓名:张三\n
        年龄:20\n
        性别:男\n
        成绩:90\n\n
        姓名:李四\n
        年龄:20\n
        性别:男\n
        成绩:88\n\n
        .....
        .....
    实现解析如下文本信息功能,返回格式为
    [
        {"姓名":"张三", "年龄":20, "性别": "男", "成绩":90},
        {"姓名":"李四", "年龄":20, "性别": "男", "成绩":88}
        .....
    ]



4.  用python编写一个函数,实现解析如下表格功能,
    <table id="content">
	    <th>
			<td>姓名</td>
			<td>年龄</td>
			<td>性别</td>
			<td>成绩</td>
		</th>
		<tr>
			<td>张三</td>
			<td>20</td>
			<td>男</td>
			<td>90</td>
		</tr>
		<tr>
			<td>李四</td>
			<td>20</td>
			<td>男</td>
			<td>88</td>
		</tr>
	</table>

    尽可能考虑全面,兼容行数,列数会发生变化的情况(title和每一行的值的列数始终相同)
    ,返回格式为

        [
            {"姓名":"张三", "年龄":20, "性别": "男", "成绩":90},
            {"姓名":"李四", "年龄":20, "性别": "男", "成绩":88}
            .....
        ] 格式;

"""
# 1.第一题
a_list = ['apple', 'banana', 'apple', 'tomato', 'orange', 'apple', 'banana', 'watermeton']
print('第一题')
for i in a_list:
    print(i, a_list.count(i))
# 2.第二题
# 请写出一段Python代码实现删除一个list里面的重复元素，不能使用set
alist = [{"name": "a", "age": 20}, {"name": "a", "age": 20}, {"name": "a", "age": 20}, {"name": "b", "age": 30},
         {"name": "c", "age": 25}, {"name": "c", "age": 25}]

x = []
for i in alist:
    if i not in x:
        x.append(i)
print('第二题')
print(x)

# 3.第三题
'''姓名: 张三\n
年龄: 20\n
性别: 男\n
成绩: 90\n\n
姓名: 李四\n
年龄: 20\n
性别: 男\n
成绩: 88\n\n'''
'''
[
        {"姓名":"张三", "年龄":20, "性别": "男", "成绩":90},
        {"姓名":"李四", "年龄":20, "性别": "男", "成绩":88}
]
'''
import re

import json


# 第三题
def test():
    a = """姓名:张三
年龄:20
性别:男
成绩:90

姓名:李四
年龄:20
性别:男
成绩:88

姓名:李四
年龄:20
性别:男
成绩:88"""
    all_lis = a.split('\n')
    # print(all_lis)
    lis = []
    dic = {}
    for i in all_lis:
        if not i:
            lis.append(dic)
            dic = dict()
        else:
            one_line = i.split(':')
            dic[one_line[0]] = one_line[1]
    # ret=json.dumps(a)
    # print(ret)
    print(lis)


print('第三题')
test()


# 4.第四题
def test4():
    import re
    from lxml import etree
    st = '''
    <table id="content">
	    <th>
			<td>姓名</td>
			<td>年龄</td>
			<td>性别</td>
			<td>成绩</td>
		</th>
		<tr>
			<td>张三</td>
			<td>20</td>
			<td>男</td>
			<td>90</td>
		</tr>
		<tr>
			<td>李四</td>
			<td>20</td>
			<td>男</td>
			<td>88</td>
		</tr>
	</table>
    '''
    key_html = etree.HTML(st)
    # print(key_html)
    all_lis = key_html.xpath('//table//td//text()')
    key_lis = all_lis[:4]
    data_lis = []
    num = len(all_lis) // 4 - 1
    # print(num)
    for i in range(num):
        sart = 4 + 4 * i
        end = sart + 4
        lis = all_lis[sart:end]
        data_lis.append(lis)

    # print(key_lis)
    # print(data_lis)
    end_lis = []
    for i in data_lis:
        dic = {}
        for my_index in range(len(i)):
            dic[key_lis[my_index]] = i[my_index]
        end_lis.append(dic)

    print(end_lis)

    # key_lis=key_st.split('')
    # print(key_lis)


print('第四题')
test4()
