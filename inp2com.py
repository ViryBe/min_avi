"""Manages ivy bus and messages"""
#!/usr/bin/env python
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

import ivy.std_api as isa
import dev_read as dr

_js = None
"""Joystick object to be used"""
_ap = True
"""Autopilot engaged"""


def nz_forward(agent, nzstr):
    """Intercept nz messages"""
    substr = "APNzControl nz="
    lbd, upb = -1, 2.5
    if update_ap():
        data = dr.saturate(float(nzstr), lbd, upb)
        isa.IvySendMsg(substr + str(data))
    else:
        data = dr.saturate(dr.nz_from_stick(_js), lbd, upb)
        isa.IvySendMsg(substr + str(data))


def p_forward(agent, pstr):
    """Intercept nz messages"""
    substr = "APLatControl rollRate="
    lbd, upb = -15, 15
    if update_ap():
        data = dr.saturate(float(pstr), lbd, upb)
        isa.IvySendMsg(substr + str(data))
    else:
        data = dr.saturate(dr.nz_from_stick(_js), lbd, upb)
        isa.IvySendMsg(substr + str(data))


def update_ap():
    """Updates _ap flag and returns it"""
    global _ap
    preap = _ap
    _ap = _ap and not dr.get_button_pushed()
    if preap is not _ap:
        isa.IvySendMsg("FCUAP1 off")
    return _ap


def on_cx_proc():
    """Launched on connection of the ivy bus"""
    global _js
    js = dr.init_js()
    _js = js


def on_die_proc():
    """Launched on closing of ivy"""
    dr.exit_pygame()

def reset_ap():
    """Sets ap to True"""
    global _ap
    _ap = True

def init_ivy():
    """Inits ivy environment"""
    app_name = "Joystick manager"
    ivy_bus = "127.255.255.255:2010"
    isa.IvyInit(app_name, "[{} ready]".format(app_name), 0, on_cx_proc,
                on_die_proc)
    isa.IvyStart(ivy_bus)
    isa.IvyBindMsg(nz_forward, r"^APNzCommand nz=(\S+)")
    isa.IvyBindMsg(p_forward, r"^APLatCommand p=(\S+)")
    isa.IvyBindMsg(lambda _, _: reset_ap(), "FCUAP1 on")
    isa.IvyMainLoop()
