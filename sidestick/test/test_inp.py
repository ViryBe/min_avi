"""Tests input from joystick"""
import _common
import ivy.std_api as isa
from sidestick import dev_read as dr

_js = None


def on_cx_proc(agent, connected):
    pass


def on_die_proc(agent, _id):
    pass


def on_msg(agent, data):
    global nz_sent
    global p_sent
    nz_sent = dr.nz_from_stick(_js)
    p_sent = dr.p_from_stick(_js)
    isa.IvySendMsg("APNzCommand nz={0}".format(nz_sent))
    isa.IvySendMsg("APLatCommand rollRate={0}".format(p_sent))


def cmp_float(x, y):
    epsilon = 1e-5
    return abs(x - y) < epsilon


def reception_nz(agent, nz_received):
    global nz_sent
    if nz_sent >= -1 and nz_sent <= 2.5:
        print (nz_sent, float(nz_received),
               cmp_float(nz_sent, float(nz_received)))
    elif nz_sent < -1:
        print (nz_sent, float(nz_received), cmp_float(-1, float(nz_received)))
    else:
        print (nz_sent, float(nz_received), cmp_float(2.5, float(nz_received)))


def reception_p(agent, p_received):
    global p_sent
    if p_sent >= -15 * _common.DEG2RAD and p_sent <= 15 * _common.DEG2RAD:
        print (p_sent, float(p_received), cmp_float(p_sent, float(p_received)))
    elif p_sent < -15 * _common.DEG2RAD:
        print (p_sent, float(p_received),
               cmp_float(-15 * _common.DEG2RAD, float(p_received)))
    else:
        print (p_sent, float(p_received),
               cmp_float(15 * _common.DEG2RAD, float(p_received)))

_js = dr.init_js()
app_name = "MyIvyApplication"
ivy_bus = "127.255.255.255:2010"
isa.IvyInit(app_name, "[%s ready]" % app_name, 0, on_cx_proc, on_die_proc)
isa.IvyStart(ivy_bus)
isa.IvyBindMsg(on_msg, "^Time t=(.*)")
isa.IvyBindMsg(reception_nz, "^APNzControl nz=(.*)")
isa.IvyBindMsg(reception_p, "^APLatControl rollRate=(.*)")
isa.IvyMainLoop()
