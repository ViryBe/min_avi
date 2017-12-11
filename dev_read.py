#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Reads input from device and outputs raw data
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

import math
import pygame

DEG2RAD = math.pi / 180
"""Constant to convert degrees to radiants"""
VAXIS = 1
"""pygame identifier of the vertical axis used"""
HAXIS = 0
"""pygame identifier of the horizontal axis"""
APBUT = 0
"""pygame identifier of the autopilot button"""
_ap = True
"""Flag indicated whether autopilot is activated"""

def init_js(jsid=0):
    """Inits pygame env

    :param jsid int: number of the joystick to use
    :returns: a ready to use joystick object
    """
    pygame.display.init()
    pygame.joystick.init()
    js = pygame.joystick.Joystick(jsid)
    js.init()
    return js


def exit_pygame():
    """Properly quits pygame"""
    pygame.joystick.quit()
    pygame.display.quit()


def saturate(insig, sbound, lbound):
    """Apply safety saturation on input signal"""
    if insig >= sbound:
        return sbound
    elif insig <= lbound:
        return lbound
    else: return insig

def nz_mapping(vaxisjs):
    """Maps output of joystick to n_z

    :param float vaxisjs:output of the joystick, \in [-1, 1]
    """
    nz = 2.5 * vaxisjs
    return nz


def p_mapping(haxisjs):
    """Maps output of joystick to a roll rate"""
    p = DEG2RAD * 1.5 * haxisjs
    return p


def nz_from_stick(js):
    """Returns the nz matching joystick manipulation"""
    return nz_mapping(js.get_axis(VAXIS))


def p_from_stick(js):
    """Returns the p matching joystick manipulation"""
    return p_mapping(js.get_axis(HAXIS))


def ap_engaged():
    """Checks whether autopilot has been disengaged"""
    global _ap
    _ap = _ap and not len(pygame.event.get(pygame.JOYBUTTONDOWN)) > 0
    return _ap


if __name__ == "__main__":
    mjs = init_js()
    print("Set button to exit program...")
    stopevt = pygame.event.wait()
    evt = None
    output = 0 + 0j
    haxisn = 0
    vaxisn = 1
    while evt != stopevt:
        evt = pygame.event.wait()
    exit_pygame()
