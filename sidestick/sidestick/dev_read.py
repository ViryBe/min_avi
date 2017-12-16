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


def saturate(insig, lbound, sbound):
    """Apply safety saturation on input signal"""
    if insig >= sbound:
        return sbound
    elif insig <= lbound:
        return lbound
    else: return insig

def nz_mapping(vaxisjs, lthrper=0.1):
    """Maps output of joystick to n_z

    :param float vaxisjs:output of the joystick, \in [-1, 1]
    """
    maxv = 2.5
    nz = maxv * vaxisjs
    return nz


def p_mapping(haxisjs, lthrper=0.1):
    """Maps output of joystick to a roll rate

    :param haxisjs: output from the joystick in [0,1]
    :param lthrper: threshold of deadzone, in percentage of the max value
                    (which is defined internally...)
    """
    maxv = 1.5 * DEG2RAD
    p = maxv * haxisjs
    return p


def nz_from_stick(js):
    """Returns the nz matching joystick manipulation"""
    return nz_mapping(js.get_axis(VAXIS))


def p_from_stick(js):
    """Returns the p matching joystick manipulation"""
    return p_mapping(js.get_axis(HAXIS))


def get_button_pushed():
    """Returns whether a button has been pushed since last call"""
    return len(pygame.event.get(pygame.JOYBUTTONDOWN)) > 0


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
