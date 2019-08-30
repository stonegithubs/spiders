a = [1,2,3,4,5,31,32,33]
b = [6,7,8,9,0]
c = ['a','b','c','d','e']
d = [11,12,13,14,15]
e = [16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
f = 1
for i in a:
    for j in b:
        for k in c:
            for l in d:
                for r in e:
                    print(i,j,k,l,r)
                    f +=1
print(f)