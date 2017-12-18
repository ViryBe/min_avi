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
"""Reads data from joystick to give scaled and verified nz and p"""

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
LASTHAXISV = 0
"""Last value of horizontal axis, in [-1, 1]"""
LASTVAXISV = 0
"""Last value of vertical axis, in [-1, 1]"""

def init_js(jsid=0):
    """Inits pygame env

    :param jsid int: number of the joystick to use
    :returns: a ready to use joystick object
    """
    pygame.init()
    pygame.display.init()
    pygame.joystick.init()
    js = pygame.joystick.Joystick(jsid)
    js.init()
    return js


def exit_pygame():
    """Properly quits pygame"""
    pygame.joystick.quit()
    pygame.display.quit()
    pygame.quit()


def saturate(insig, lbound, sbound):
    """Apply safety saturation on input signal"""
    if insig >= sbound:
        return sbound
    elif insig <= lbound:
        return lbound
    else: return insig

def nz_mapping(vaxisjs, lthrper=0.1):
    """Maps output of joystick to n_z

    :param float vaxisjs:output of the joystick, in [-1, 1]
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
    maxv = 15 * DEG2RAD
    p = maxv * haxisjs
    return p


def extract_evt(evtype, axis, defval):
    """More precise event extractor from the queue

    :param int evtype: an Event type object
    :param int axis: the number of the axis
    :returns: the mean of the values since the previous call and last value
    """
    axisinp = pygame.event.get(evtype)
    # Not kept events, will be put back in the queue
    notkept = [e for e in axisinp if e.axis != axis]
    map(pygame.event.post, notkept)
    kept = [e for e in axisinp if e.axis == axis]
    kval = [e.value for e in kept]
    kmean = sum(kval)/len(kval) if len(kval) > 0 else defval
    lval = kval[-1] if len(kval) > 0 else defval
    return kmean, lval


def nz_from_stick(js, lthresh=0.1):
    """Returns the nz matching joystick manipulation

    :param float lthresh: low threshold defining a deadzone around null point
                          of the joystick
    """
    vaxismean, linp = extract_evt(pygame.JOYAXISMOTION, VAXIS, LASTVAXISV)
    global LASTVAXISV
    LASTVAXISV = linp
    return nz_mapping(vaxismean) if abs(vaxismean) > lthresh else 0


def p_from_stick(js, lthresh=0.1):
    """Returns the p matching joystick manipulation
    :param float lthresh: low threshold defining a deadzone around null point
                          of the joystick
    """
    haxismean, linp = extract_evt(pygame.JOYAXISMOTION, HAXIS, LASTHAXISV)
    global LASTHAXISV
    LASTHAXISV = linp
    return p_mapping(haxismean) if abs(haxismean) > lthresh else 0


def get_button_pushed():
    """Returns whether a button has been pushed since last call"""
    return len(pygame.event.get(pygame.JOYBUTTONDOWN)) > 0
