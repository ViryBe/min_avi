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


def query_jstate(js):
    """Queries the state of the joystick

    :param js: joystick to query
    :type js: :class:`py.pygame.joystick.Joystick
    """
    haxisn = 0
    vaxisn = 1
    return js.get_axis(haxisn) + 1j * js.get_axis(vaxisn)


def mapping(x_stick, y_stick, nz_sat_inf=-1):
    """
    x_stick \in [-1, 1] -> [-15, 15] °/sec
    y_stick \in [-1, 1] -> [2,5, -1]
    """
    nz = 2.5 * y_stick
    p = DEG2RAD * 1.5 * x_stick
    return (nz if nz >= nz_sat_inf else nz_sat_inf, p)


if __name__ == "__main__":
    js = init_js()
    print("Set button to exit program...")
    stopevt = pygame.event.wait()
    evt = None
    output = 0 + 0j
    haxisn = 0
    vaxisn = 1
    while evt != stopevt:
        evt = pygame.event.wait()
        output = query_jstate(js)
        print(output)
    exit_pygame()
