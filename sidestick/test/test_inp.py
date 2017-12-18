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
    nz_sent = dr.nz_from_stick(_js)
    p_sent = dr.p_from_stick(_js)
    isa.IvySendMsg("APNzCommand nz={0}".format(nz_sent))
    isa.IvySendMsg("APLatCommand p={0}".format(p_sent))


def reception_nz(agent, nz_received):
    print("nz: {}".format(nz_received))


def reception_p(agent, p_received):
    print("p: {}".format(p_received))


_js = dr.init_js()
app_name = "MyIvyApplication"
ivy_bus = "127.255.255.255:2010"
isa.IvyInit(app_name, "[%s ready]" % app_name, 0, on_cx_proc, on_die_proc)
isa.IvyStart(ivy_bus)
isa.IvyBindMsg(on_msg, "^Time t=(.*)")
isa.IvyBindMsg(reception_nz, "^APNzControl nz=(.*)")
isa.IvyBindMsg(reception_p, "^APLatControl rollRate=(.*)")
isa.IvyMainLoop()
