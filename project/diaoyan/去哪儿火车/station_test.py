def get_station():
    with open('./station_info.txt','r',encoding='utf8')as f:
        content = f.read()
    station_list = content.split()
    a = 1
    for i in station_list:
        for j in station_list:
            if i == j:
                continue
            else:
                print(i,j)
