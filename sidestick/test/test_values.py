"""
POURQUOI CE TEST ?
qu'est ce qui est enoyer ? pourquoi ?
qu'est ce qui est recu ?
qu'est ce qui est afficher ?
interet de ce test ?
"""

"""Tests saturation and forward with autopilot engaged, generating 10 random
values"""


from sys import argv, exit
import math
import random as rd
from ivy.std_api import *
import time

DEG2RAD = math.pi/180


# le test est lancé avec un paramètre nz ou p
if len(argv) == 1:
    print("il faut 1 argument : 'nz' ou 'p'")
    sys.exit()
elif argv[1] == "nz":
    BORNE = 5
    VALUE_MIN = -1
    VALUE_MAX = 2.5
    type1 = "Nz"
    type2 = "nz"
    type3 = "nz"
elif argv[1] == "p":
    BORNE = 30*DEG2RAD
    VALUE_MIN = -15*DEG2RAD
    VALUE_MAX = 15*DEG2RAD
    type1 = "Lat"
    type2 = "rollRate"
    type3 = "p"
else :
    print("mauvais argument 'nz' ou 'p'")
    sys.exit()

# fin de l'initialkisation de l'environnement
# ============================================

def rslt():
    with open('rslt.txt', 'w') as file:
        for sent,rcvd in zip(values_sent, values_received):
            if sent >= VALUE_MIN and sent <= VALUE_MAX:
                file.write(sent, float(rcvd), cmp_float(float(rcvd), float(sent)))
                # print(sent, float(rcvd), cmp_float(float(rcvd), float(sent)))
            elif sent < VALUE_MIN :
                file.write(sent, float(rcvd), cmp_float(float(rcvd), float(VALUE_MIN)))
                # print(sent, float(rcvd), cmp_float(float(rcvd), float(VALUE_MIN)))
            else :
                file.write(sent, float(rcvd), cmp_float(float(rcvd), float(VALUE_MAX)))
                # print(sent, float(rcvd), cmp_float(float(rcvd), float(VALUE_MAX)))

def on_cx_proc(agent, connected):
    pass

def on_die_proc(agent, _id):
    pass

def on_msg(agent, data):
    global values_received
    values_received.append(data)
    # quand tout les messages on été envoyer et recu, on peut les comparer
    # et obtenir les resutats avec la fonciton rslt()
    if (len(values_received) == 10):
        rslt()


app_name = "Test"
ivy_bus="127.255.255.255:2010"
IvyInit(app_name, "[%s ready]" % app_name, 0, on_cx_proc, on_die_proc)
IvyStart(ivy_bus)
time.sleep(5)
IvyBindMsg(on_msg, "^AP{0}Control {1}=(.*)".format(type1,type2))


values_sent = [rd.uniform(-BORNE, BORNE) for i in range(10)]
for i in values_sent:
    IvySendMsg("AP{0}Command {1}={2}".format(type1,type3,i))

values_received = []

def cmp_float(x, y):
    epsilon = 1e-5
    return abs(x-y) < epsilon

IvyMainLoop()
