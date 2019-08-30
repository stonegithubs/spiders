station_list = [1,2,3,4,5]

for i in station_list:
    for j in station_list:
        if i == j:
            continue
        else:
            print(i,j)
