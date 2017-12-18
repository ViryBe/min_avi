# -*- coding: utf-8 -*-
#
#    Transforms raw input data to aircraft commands
#    Copyright (C) 2017  Gabriel Hondet, Benoit Viry, Damien Thoral, Nicolas
#    Soulard
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Manages ivy bus and messages"""

import math
import ivy.std_api as isa
import dev_read as dr
import time
from pydub import AudioSegment
from pydub.playback import play

DEG2RAD = math.pi / 180.
_js = None
"""Joystick object to be used"""
_ap = True
"""Autopilot engaged"""
_sound = AudioSegment.from_wav("../data/Autopilot.wav")
"""Audio file to play when disabling auto pilot"""

def nz_forward(agent, nzstr):
    """Intercept nz messages"""
    substr = "APNzControl nz="
    lbd, upb = -1, 2.5
    if update_ap():
        data = dr.saturate(float(nzstr), lbd, upb)
        print(substr + str(data))
        isa.IvySendMsg(substr + str(data))
    else:
        data = dr.saturate(dr.nz_from_stick(_js), lbd, upb)
        isa.IvySendMsg(substr + str(data))


def p_forward(agent, pstr):
    """Intercept p messages"""
    substr = "APLatControl rollRate="
    lbd, upb = -DEG2RAD * 15, DEG2RAD * 15
    if update_ap():
        data = dr.saturate(float(pstr), lbd, upb)
        print(substr + str(data))
        isa.IvySendMsg(substr + str(data))
    else:
        data = dr.saturate(dr.p_from_stick(_js), lbd, upb)
        print(substr + str(data))
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


def reset_ap(agent, toto):
    """Sets ap to True"""
    global _ap
    _ap = True


def init_ivy():
    """Inits ivy environment"""
    app_name = "Mini_manche"
    ivy_bus = "127.255.255.255:2010"
    isa.IvyInit(app_name, "[{} ready]".format(app_name), 0, on_cx_proc,
                on_die_proc)
    isa.IvyStart(ivy_bus)
    time.sleep(1)
    isa.IvyBindMsg(nz_forward, "^APNzCommand nz=(.*)")
    isa.IvyBindMsg(p_forward, "^APLatCommand p=(.*)")
    isa.IvyBindMsg(reset_ap, "FCUAP1 on")
    isa.IvyBindMsg(switch_fcu, "FCUAP1 push")
    isa.IvyMainLoop()
