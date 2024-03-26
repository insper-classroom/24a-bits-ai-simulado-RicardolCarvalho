#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

from myhdl import *


def exe1(a, b, c, s):
    @always_comb
    def comb():
        s.next = (a and b and c) or ((not((not a) and (not c))) and (a and (not b)))
    return instances()


def exe2(l, m, h, l_vd, l_am, l_vm, l_az, l_lj):
    @always_comb
    def comb():
        l_vd.next = l and not m and not h
        l_am.next = l and m and not h
        l_vm.next = l and m and h
        l_az.next = not l and not m and not h
        l_lj.next = (h and (not l or not m)) or (m and not l)

    return instances()


def exe3(i3, i2, i1, i0, p1, p0, v):
    @always_comb
    def comb():
        p1.next = i3 or i2
        p0.next = ((not i3) and (not i2) and i1) or (i3)
        v.next = i3 or i2 or i1 or i0

    return instances()


def exe4_simulando(a, b, c, d, e, f, g, h, i, j, k, l):
    @always_comb
    def comb():
        b1 = Signal(bool(0))
        a.next = 1
        b.next = 1
        sub1 = exe4_half_sub(a,b,c,i)
        d.next = 1
        e.next = 1
        sub2 = exe4_full_sub(d,e,c,f,j)
        g.next = 1
        h.next = 0
        sub3 = exe4_full_sub(g,h,b1,k)
        k.next = 0

    return instances()


def exe4_half_sub(x, y, b, d):
    @always_comb
    def comb():
        d.next = x ^ y
        b.next = (not x) and y

    return instances()


def exe4_full_sub(x, y, z, b, d):
    @always_comb
    def comb():
        d.next = (((not x) and (not y) and z) or ((not x) and y and (not z)) 
                  or (x and (not y) and (not z)) or (x and y and z))
        b.next = ((not x) and y) or ((not x) and z) or (y and z)
    return instances()


def exe4_sub3(v2, v1, v0, p2, p1, p0, q2, q1, q0):
    b3, b2, b1 = [Signal(bool(0)) for i in range(3)]

    c0 = exe4_half_sub(v0, p0, b1, q0)
    c1 = exe4_full_sub(v1, p1, b1, b2, q1)
    c2 = exe4_full_sub(v2, p2, b2, b3, q2)
    return instances()
