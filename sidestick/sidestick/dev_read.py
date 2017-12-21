"""Reads data from joystick to give scaled and verified nz and p"""

import math
import pygame

DEG2RAD = math.pi / 180
"""Constant to convert degrees to radiants"""
LIM_P = 15 * DEG2RAD
LIM_NZ_MIN = -1
LIM_NZ_MAX = 2.5
LIM_PHI_AP = 30 * DEG2RAD
LIM_PHI_MAN= 66 * DEG2RAD
"""list of constants/limitations"""
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
"""dict with last values from the stick """

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
    """Apply safety saturation on input signal:
    ret \in [lbound, sbound]
    """
    return (insig if lbound <= insig <= sbound
            else lbound if insig < lbound else sbound)

def nz_mapping(vaxisjs, lthrper=0.01):
    """Maps output of joystick to n_z

    :param float vaxisjs:output of the joystick, in [-1, 1]
    """
    maxv = LIM_NZ_MAX
    nz = maxv * vaxisjs + 1
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
    :returns: nada
    """
    axisinp = pygame.event.get(evtype)

    global JOY_INP
    # we store all from the stick in according to the axis
    JOY_INP["p"]  += [e.value for e in axisinp if e.axis == HAXIS]
    JOY_INP["nz"] += [e.value for e in axisinp if e.axis == VAXIS]


def nz_from_stick(js, lthresh=0.01):
    """Returns the nz matching joystick manipulation

    :param float lthresh: low threshold defining a deadzone around null point
                          of the joystick
    """
    global LASTVAXISV
    extract_evt(pygame.JOYAXISMOTION)
    val = JOY_INP["nz"][-1] if len(JOY_INP["nz"]) > 0 else LASTVAXISV
    LASTVAXISV = val
    JOY_INP["nz"] = []
    return nz_mapping(val) if abs(val) > lthresh else 1


def p_from_stick(js, lthresh=0.05):
    """Returns the p matching joystick manipulation
    :param float lthresh: low threshold defining a deadzone around null point
                          of the joystick
    """
    global LASTHAXISV
    extract_evt(pygame.JOYAXISMOTION)
    val = JOY_INP["p"][-1] if len(JOY_INP["p"]) > 0 else LASTHAXISV
    LASTHAXISV = val
    JOY_INP["p"] = []
    return p_mapping(val) if abs(val) > lthresh else 0


def get_button_pushed():
    """Returns whether a button has been pushed since last call"""
    return len(pygame.event.get(pygame.JOYBUTTONDOWN)) > 0
