with open('./station_info.txt','r',encoding='utf8')as f:
    res = f.readlines()
    # print(res[::-1])
    for i in res[::-1]:
        with open('./station.txt','a',encoding='utf8')as f:
            f.write(i)
        # print(i.replace('\n',''))