# with open('./table_hotel.txt','r',encoding='utf8')as f:
#     lines = f.read()
#     # print(lines.replace('''
# 	# 			''',''))
#     with open('./table_hotel1.txt','w',encoding='utf8')as j:
#         j.write(lines.replace('''
# 				''',''))
with open('./table_hotel1.txt','r',encoding='utf8')as k:
    liness = k.readlines()
    for i in liness:
        index = i[0]
        if index == '"':
            lines=i
            continue
        else:
            lines = i[1:]
        with open('./table_hotel1.txt', 'a', encoding='utf8')as j:
            j.write(lines)
    # for i in lines:
    #     print(i)