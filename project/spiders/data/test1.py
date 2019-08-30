# import copy
# a = (1, 2,[3])
# # b = [4,5,6]
# # for i in b:
# #     a.append(i)
# #     c = list(set(a))
# # print(c)
# # A0 = dict(zip(a, b))
# # print(A0)
# print(id(a))
# b = copy.copy(a)
# # b = a.copy()
# a[2].append('4')
# print(id(a))
# print(id(b))
#
# # c = [1, 2, [4, 4]]
# # print(id(c))
# # d = c
# # d[0]=7
# # d[2][0]=3
# # print(c)
# # print(id(c))
# # print(id(d))
ls1 = [1, 2, 5, 4, 2, 4, 7, 8, 3]
ls3 = []
for i in ls1:
    ls2 = []
    for j in ls1:
        if i + j == 6:
            if i == j:
                break
            ls2.append(i)
            ls2.append(j)
            if ls2:
                if ls2 in ls3:
                    break
                ls3.append(ls2)
                # print(ls2)
            break
print(ls3)
