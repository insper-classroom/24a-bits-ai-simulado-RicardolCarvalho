#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from myhdl import *
from componentes import *
import pytest
import os

try:
    from telemetry import telemetryMark

    pytestmark = telemetryMark()
except ImportError as err:
    print("Telemetry não importado")


def source(name):
    dir = os.path.dirname(__file__)
    src_dir = os.path.join(dir, ".")
    return os.path.join(src_dir, name)

vec_exe1 = ["0000", "0010", "0100", "0110", "1001", "1011", "1100", "1111"]


@pytest.mark.telemetry_files(source("componentes.py"))
def test_exe1_a():
    @instance
    def stimulus():
        for t in vec_exe1:
            a.next = int(t[0])
            b.next = int(t[1])
            c.next = int(t[2])
            yield delay(1)
            assert s == int(t[3])

    a, b, c, s = [Signal(bool(0)) for i in range(4)]
    dut = exe1(a, b, c, s)
    sim = Simulation(dut, stimulus)
    sim.run()

vec_exe2 = [
    "00100001",
    "01000001",
    "01100001",
    "10010000",
    "10100001",
    "11001000",
    "11100100",
    "00000010",
]

@pytest.mark.telemetry_files(source("componentes.py"))
def test_exe2():
    @instance
    def stimulus():
        for t in vec_exe2:
            l.next = int(t[0])
            m.next = int(t[1])
            h.next = int(t[2])
            yield delay(1)
            assert l_vd == int(t[3])
            assert l_am == int(t[4])
            assert l_vm == int(t[5])
            assert l_az == int(t[6])
            assert l_lj == int(t[7])

    l, m, h, l_vd, l_am, l_vm, l_az, l_lj = [Signal(bool(0)) for i in range(8)]
    dut = exe2(l, m, h, l_vd, l_am, l_vm, l_az, l_lj)
    sim = Simulation(dut, stimulus)
    sim.run()

vec_exe3 = ["0001001", "0011011", "0101101", "1110111"]

@pytest.mark.telemetry_files(source("componentes.py"))
def test_exe3():
    @instance
    def stimulus():
        t = "0000"
        i3.next = int(t[3])
        i2.next = int(t[2])
        i1.next = int(t[1])
        i0.next = int(t[0])
        yield delay(1)
        assert v == 0

        for test in vec_exe3:
            print(test)
            i3.next = int(test[0])
            i2.next = int(test[1])
            i1.next = int(test[2])
            i0.next = int(test[3])

            yield delay(1)
            assert int(p1) == int(test[4])
            assert int(p0) == int(test[5])
            assert int(v) == int(test[6])

    i3, i2, i1, i0, p1, p0, v = [Signal(bool(0)) for i in range(7)]
    dut = exe3(i3, i2, i1, i0, p1, p0, v)
    sim = Simulation(dut, stimulus)
    sim.run()


vec_exe4_half = ["0000", "0111", "1001", "1100"]


@pytest.mark.telemetry_files(source("componentes.py"))
def test_exe4_half_sub():
    @instance
    def stimulus():
        for test in vec_exe4_half:
            x.next = int(test[0])
            y.next = int(test[1])
            yield delay(1)
            assert int(b) == int(test[2])
            assert int(d) == int(test[3])

    x, y, b, d = [Signal(bool(0)) for i in range(4)]
    dut = exe4_half_sub(x, y, b, d)
    sim = Simulation(dut, stimulus)
    sim.run()


vec_exe4_full = ["00000", "00111", "01011", "01110", "10001", "10100", "11000", "11111"]


@pytest.mark.telemetry_files(source("componentes.py"))
def test_exe4_full_sub():
    @instance
    def stimulus():
        for test in vec_exe4_full:
            x.next = int(test[0])
            y.next = int(test[1])
            z.next = int(test[2])

            yield delay(1)
            assert int(b) == int(test[3])
            assert int(d) == int(test[4])

    x, y, z, b, d = [Signal(bool(0)) for i in range(5)]
    dut = exe4_full_sub(x, y, z, b, d)
    sim = Simulation(dut, stimulus)
    sim.run()


@pytest.mark.telemetry_files(source("componentes.py"))
def test_exe4_sub3():
    @instance
    def stimulus():
        # -1 - -1
        v2.next = 1
        v1.next = 1
        v0.next = 1
        p2.next = 1
        p1.next = 1
        p0.next = 1

        yield delay(1)
        assert int(q2) == 0
        assert int(q1) == 0
        assert int(q0) == 0

        # 0 - -1
        v2.next = 0
        v1.next = 0
        v0.next = 0
        p2.next = 1
        p1.next = 1
        p0.next = 1

        yield delay(1)
        assert int(q2) == 0
        assert int(q1) == 0
        assert int(q0) == 1

        # 2 - 1
        v2.next = 0
        v1.next = 1
        v0.next = 0
        p2.next = 0
        p1.next = 0
        p0.next = 1

        yield delay(1)
        assert int(q2) == 0
        assert int(q1) == 0
        assert int(q0) == 1

    v2, v1, v0 = [Signal(bool(0)) for i in range(3)]
    p2, p1, p0 = [Signal(bool(0)) for i in range(3)]
    q2, q1, q0 = [Signal(bool(0)) for i in range(3)]
    dut = exe4_sub3(v2, v1, v0, p2, p1, p0, q2, q1, q0)

    sim = Simulation(dut, stimulus)
    sim.run()
