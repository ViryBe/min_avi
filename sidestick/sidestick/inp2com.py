"""Manages ivy bus and messages"""

import ivy.std_api as isa
import dev_read as dr
from dev_read import DEG2RAD, LIM_NZ_MIN, LIM_NZ_MAX
import time
from pydub import AudioSegment
from pydub.playback import play


_js = None
"""Joystick object to be used"""
_ap = False
"""Autopilot engaged"""
_sound = AudioSegment.from_wav("../data/Autopilot.wav")
"""Audio file to play when disabling auto pilot"""
_phi = 0
"""current phi position (for safety net)"""

def nz_forward(agent, nzstr):
    """Intercept nz messages"""
    substr = "APNzControl nz="
    lbd, upb = -1, 2.5

    data = (dr.saturate(float(nzstr), lbd, upb)
            if update_ap()
            else dr.saturate(dr.nz_from_stick(_js), lbd, upb))

    isa.IvySendMsg(substr + str(data))


def p_forward(agent, pstr):
    """Intercept p messages"""
    substr = "APLatControl rollRate="
    lbd, upb = -dr.LIM_P, dr.LIM_P
    if update_ap():
        # limitation 30° if in PA
        data = (dr.saturate(float(pstr), lbd, upb)
                if not (abs(_phi) > 30 * DEG2RAD)
                else 0)
    else:
        # limitation 66° if in PA
        data = (dr.saturate(dr.p_from_stick(_js), lbd, upb)
                if not (abs(_phi) > 66 * DEG2RAD)
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
    global _ap
    _ap = not _ap
    msg = "FCUAP1 " + ("on" if _ap else "off")
    isa.IvySendMsg(msg)
    if not _ap:
        play(_sound)


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
