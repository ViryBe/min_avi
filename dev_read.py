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

import pygame

# Inits
pygame.display.init()
pygame.joystick.init()

js = pygame.joystick.Joystick(0)
js.init()

print("Set button to exit program...")
stopevt = pygame.event.wait()
evt = None
output = 0 + 0j
haxisn = 0
vaxisn = 1
while evt != stopevt:
    evt = pygame.event.wait()
    output = js.get_axis(haxisn) + 1j * js.get_axis(vaxisn)
    print(output)
pygame.joystick.quit()
pygame.display.quit()
