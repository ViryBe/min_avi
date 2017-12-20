"""Reads data from joystick to give scaled and verified nz and p"""

import math
import pygame

DEG2RAD = math.pi / 180
LIM_P = DEG2RAD * 15
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

JOY_INP = {"p" : [], "nz" : []}

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

def nz_mapping(vaxisjs, lthrper=0.05):
    """Maps output of joystick to n_z

    :param float vaxisjs:output of the joystick, in [-1, 1]
    """
    maxv = 2.5
    nz = maxv * vaxisjs
    return nz


def p_mapping(haxisjs, lthrper=0.05):
    """Maps output of joystick to a roll rate

    :param haxisjs: output from the joystick in [0,1]
    :param lthrper: threshold of deadzone, in percentage of the max value
                    (which is defined internally...)
    """
    maxv = LIM_P
    p = maxv * haxisjs
    return p


def extract_evt(evtype):
    """More precise event extractor from the queue

    :param int evtype: an Event type object
    :param int axis: the number of the axis
    :returns: the mean of the values since the previous call and last value
    """
    axisinp = pygame.event.get(evtype)
    global JOY_INP
    # Not kept events, will be put back in the queue
    JOY_INP["p"]  += [e.value for e in axisinp if e.axis == HAXIS]
    JOY_INP["nz"] += [e.value for e in axisinp if e.axis == VAXIS]


def nz_from_stick(js, lthresh=0.05):
    """Returns the nz matching joystick manipulation

    :param float lthresh: low threshold defining a deadzone around null point
                          of the joystick
    """
    global LASTVAXISV
    extract_evt(pygame.JOYAXISMOTION)
    val = sum(JOY_INP["nz"]) / len(JOY_INP["nz"]) if len(JOY_INP["nz"]) > 0 else LASTVAXISV
    LASTVAXISV = val
    JOY_INP["nz"] = []
    return nz_mapping(val) if abs(val) > lthresh else 0


def p_from_stick(js, lthresh=0.05):
    """Returns the p matching joystick manipulation
    :param float lthresh: low threshold defining a deadzone around null point
                          of the joystick
    """
    global LASTHAXISV
    extract_evt(pygame.JOYAXISMOTION)
    val = sum(JOY_INP["p"]) / len(JOY_INP["p"]) if len(JOY_INP["p"]) > 0 else LASTHAXISV
    LASTHAXISV = val
    JOY_INP["p"] = []
    return p_mapping(val) if abs(val) > lthresh else 0


def get_button_pushed():
    """Returns whether a button has been pushed since last call"""
    return len(pygame.event.get(pygame.JOYBUTTONDOWN)) > 0
