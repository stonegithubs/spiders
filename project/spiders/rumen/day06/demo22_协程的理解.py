"""
def test1():
    print("--1--")
    yield 10
    print("--2--")


t1 = test1()
print(type(t1))

print(next(t1))
"""


"""
def test1():
    while True:
        print("--1--")
        n = yield 10
        print("--%s--"%n)


t1 = test1()
next(t1)
t1.send(100)
"""



"""
def test1():
    while True:
        yield "--1--"

def test2():
    while True:
        yield "--2--"

t1 = test1()
t2 = test2()
while True:
    print(next(t1))
    print(next(t2))
"""





