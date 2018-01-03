"""Manages ivy bus and messages"""

import ivy.std_api as isa
import dev_read as dr
from dev_read import (DEG2RAD,
                      LIM_NZ_MIN,
                      LIM_NZ_MAX,
                      LIM_PHI_AP,
                      LIM_PHI_MAN)
import time
from pydub import AudioSegment
from pydub.playback import play

import threading

class Button_Pushed(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        """
        we always need to listen for a pus button not only when we receved
        a msg. eg when the simulation is in pause
        """
        while True:
            update_ap()


_js = None
"""Joystick object to be used"""
_ap = True
"""Autopilot engaged ? (ap engaged for take off)"""
_sound = AudioSegment.from_wav("../data/Autopilot.wav")
"""Audio file to play when disabling auto pilot"""
_phi = 0
"""current phi position (for safety net)"""

def nz_forward(agent, nzstr):
    """Intercept nz messages"""
    substr = "APNzControl nz="
    lb, up = LIM_NZ_MIN, LIM_NZ_MAX

    data = dr.saturate((float(nzstr) if _ap else dr.nz_from_stick(_js)), lb, up)
    isa.IvySendMsg(substr + str(data))


def p_forward(agent, pstr):
    """Intercept p messages"""
    substr = "APLatControl rollRate="
    lb, up = -dr.LIM_P, dr.LIM_P
    if _ap:
        # limitation 30° if in PA
        data = (dr.saturate(float(pstr), lb, up)
                if abs(_phi) < LIM_PHI_AP
                else 0)
    else:
        # limitation 66° if not in PA
        data = (dr.saturate(dr.p_from_stick(_js), lb, up)
                if abs(_phi) < LIM_PHI_MAN
                else 0)
    isa.IvySendMsg(substr + str(data))


def update_ap():
    """Updates _ap flag and returns it"""
    global _ap
    preap = _ap
    _ap = _ap and not dr.get_button_pushed()
    if preap is not _ap:
        isa.IvySendMsg("FCUAP1 off")
        play(_sound)
    return _ap


def switch_fcu(agent):
    """
    manage the autopilot when the  pilot push ap button
    if |phi| > 30° the ap cannot be engaged
    """
    global _ap
    if abs(_phi) < LIM_PHI_AP: # plane nedds to be in ap flight domain in order to switch
        _ap = not _ap
        msg = "FCUAP1 " + ("on" if _ap else "off")
        isa.IvySendMsg(msg)
        if not _ap:
            play(_sound)
    else: # if the plane isn't in ap flight domain, do nothing
        pass


def on_cx_proc(*argv):
    """Launched on connection of the ivy bus"""
    global _js
    js = dr.init_js()
    _js = js


def on_die_proc(*argv):
    """Launched on closing of ivy"""
    dr.exit_pygame()


def reset_ap(*argv):
    """Sets ap to True"""
    global _ap
    _ap = True


def update_phi(agent, phi):
    """
    we need to track the value of phi (from state vector) in order to
    implement a basic safty net
    """
    global _phi
    _phi = float(phi)


def init_ivy():
    """Inits ivy environment"""
    app_name = "Mini_manche"
    ivy_bus = "127.255.255.255:2010"
    isa.IvyInit(app_name, "[{} ready]".format(app_name), 0, on_cx_proc,
                on_die_proc)
    isa.IvyStart(ivy_bus)
    time.sleep(2)

    isa.IvyBindMsg(nz_forward, "^APNzCommand nz=(.*)")
    isa.IvyBindMsg(p_forward, "^APLatCommand p=(.*)")
    isa.IvyBindMsg(reset_ap, "FCUAP1 on")
    isa.IvyBindMsg(switch_fcu, "FCUAP1 push")
    isa.IvyBindMsg(update_phi, "StateVector x=.* y=.* Vp=.* fpa=.* psi=.* phi=(.*)")
    isa.IvyMainLoop()
