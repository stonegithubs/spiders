def test1():
    while True:
        budget_cap = int(input("请输入预算上限："))
        if 0< budget_cap < 10000:
            break
        else:
            print("请输入一个小于10000的整数：")

    price_lst0 = input("请输入价格并用空格隔开：")
    price_lst1 = price_lst0.split(" ")
    price_lst = []
    for i in price_lst1:
        if 0< int(i) < 10000:
            price_lst.append(int(i))
        else:
            print("价格输入错误！")
    price_lst.sort()

    sum,x = 0,0
    for x in price_lst:
        if budget_cap >= x:
            budget_cap -= x
            sum += x
        else:
            break
    print(sum)


if __name__ == '__main__':
    test1()
