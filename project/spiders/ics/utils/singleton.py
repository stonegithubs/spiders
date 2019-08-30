#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'wu_yong'


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


if __name__ == '__main__':

    class A(Singleton):
        a = 1

        def __init__(self, x=0):
            self.x = x

    # class A(object):
    #     __metaclass__ = Singleton
    #     a = 1
    #
    #     def __init__(self, x=0):
    #         self.x = x
    a1 = A(2)
    a2 = A(3)
    print a1
    print a2
    print id(a1)
    print id(a2)
    print id(A(4))
    print id(A(6))