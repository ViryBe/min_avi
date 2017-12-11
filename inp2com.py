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

_ap = True
"""Whether the autopilot is activated"""
_js = None
"""Joystick object to be used"""


def nz_forward(agent, nzstr):
    """Intercept nz messages"""
    substr = "APNzControl nz="
    lbd, upb = -1, 2.5
    if _ap:
        data = dr.saturate(float(nzstr), lbd, upb)
        isa.IvySendMsg(substr + str(data))
    else:
        data = dr.saturate(dr.nz_from_stick(_js), lbd, upb)
        isa.IvySendMsg(substr + str(data))


def p_forward(agent, pstr):
    """Intercept nz messages"""
    substr = "APLatControl rollRate="
    lbd, upb = -15, 15
    if _ap:
        data = dr.saturate(float(pstr), lbd, upb)
        isa.IvySendMsg(substr + str(data))
    else:
        data = dr.saturate(dr.nz_from_stick(_js), lbd, upb)
        isa.IvySendMsg(substr + str(data))


def on_cx_proc():
    """Launched on connection of the ivy bus"""
    global _js
    js = dr.init_js()
    _js = js


def on_die_proc():
    """Launched on closing of ivy"""
    dr.exit_pygame()

def init_ivy():
    """Inits ivy environment"""
    app_name = "Joystick manager"
    ivy_bus = "127.255.255.255:2010"
    isa.IvyInit(app_name, "[{} ready]".format(app_name), 0, on_cx_proc,
                on_die_proc)
    isa.IvyStart(ivy_bus)
    isa.IvyBindMsg(nz_forward, r"^APNzCommand nz=(\S+)")
    isa.IvyBindMsg(p_forward, r"^APLatCommand p=(\S+)")
    isa.IvyMainLoop()
