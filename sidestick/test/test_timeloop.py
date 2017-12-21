"""
POURQUOI CE TEST ?
qu'est ce qui est enoyer ? pourquoi ?
qu'est ce qui est recu ?
qu'est ce qui est afficher ?
interet de ce test ?
"""


from ivy.std_api import *
import random as rd
from math import pi

DEG2RAD = pi/180

def on_cx_proc(agent, connected):
    pass


def on_die_proc(agent, _id):
    pass


def on_msg(agent, data):
    global nz_sent
    global p_sent
    nz_sent = rd.uniform(-5,5)
    p_sent = rd.uniform(-30*DEG2RAD, 30*DEG2RAD)
    IvySendMsg("APNzCommand nz={0}".format(nz_sent))
    IvySendMsg("APLatCommand rollRate={0}".format(p_sent))

def cmp_float(x, y):
    epsilon = 1e-5
    return abs(x-y) < epsilon

def reception_nz(agent, nz_received):
    global nz_sent
    if nz_sent >= -1 and nz_sent <= 2.5:
        print (nz_sent, float(nz_received), cmp_float(nz_sent, float(nz_received)))
    elif nz_sent < -1:
        print (nz_sent, float(nz_received), cmp_float(-1, float(nz_received)))
    else:
        print (nz_sent, float(nz_received), cmp_float(2.5, float(nz_received)))

def reception_p(agent, p_received):
    global p_sent
    if p_sent >= -15*DEG2RAD and p_sent <= 15*DEG2RAD:
        print (p_sent, float(p_received), cmp_float(p_sent, float(p_received)))
    elif p_sent < -15*DEG2RAD:
        print (p_sent, float(p_received), cmp_float(-15*DEG2RAD, float(p_received)))
    else:
        print (p_sent,float(p_received), cmp_float(15*DEG2RAD,float(p_received)))



app_name = "MyIvyApplication"
ivy_bus="127.255.255.255:2010"
IvyInit(app_name, "[%s ready]" % app_name, 0, on_cx_proc, on_die_proc)
IvyStart(ivy_bus)
IvyBindMsg(on_msg, "^Time t=(.*)")
IvyBindMsg(reception_nz, "^APNzControl nz=(.*)")
IvyBindMsg(reception_p, "^APLatControl rollRate=(.*)")
IvyMainLoop()
