# Credit for a lot of the code: https://github.com/matlo/gimx-network-client
# Credit for PS4 pygame connection: https://gist.github.com/claymcleod/028386b860b75e4f5472
import socket
import struct
import sys
import os
import pprint
import pygame
import time
from enum import IntEnum
from time import sleep

DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 51914


class Ps4Controls(IntEnum):
    LEFT_STICK_X = 0
    LEFT_STICK_Y = 1
    RIGHT_STICK_X = 2
    RIGHT_STICK_Y = 3
    FINGER1_X = 4
    FINGER1_Y = 5
    FINGER2_X = 6
    FINGER2_Y = 7
    SHARE = 128
    OPTIONS = 129
    PS = 130
    UP = 131
    RIGHT = 132
    DOWN = 133
    LEFT = 134
    TRIANGLE = 135
    CIRCLE = 136
    CROSS = 137
    SQUARE = 138
    L1 = 139
    R1 = 140
    L2 = 141
    R2 = 142
    L3 = 143
    R3 = 144
    TOUCHPAD = 145
    FINGER1 = 146
    FINGER2 = 147


class ButtonState(IntEnum):
    RELEASED = 0
    PRESSED = 255


def send_message(ip, port, changes):
    packet = bytearray([0x01, len(changes)])  # type + axis count

    for axis, value in changes.items():
        # axis + value (network byte order)
        packet.extend(
            [axis, (value & 0xff000000) >> 24, (value & 0xff0000) >> 16, (value & 0xff00) >> 8, (value & 0xff)])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(packet, (ip, port))


def check_status(ip, port):
    packet = bytearray([0x00, 0x00])
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((ip, port))
    sock.send(packet)
    timeval = struct.pack('ll', 1, 0)  # seconds and microseconds
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeval)
    try:
        data, (address, port) = sock.recvfrom(2)
        response = bytearray(data)
        if response[0] != 0x00:
            print("Invalid reply code: {0}".format(response[0]))
            return 1
    except socket.error as err:
        print(err)

    return 0


ip = DEFAULT_IP
port = DEFAULT_PORT

if check_status(ip, port):
    sys.exit(-1)


def bool_to_button(_bool):
    return int(_bool)


def parse_button_dict(button_dict):
    """
    Returns a dict with the names of the buttons as keys and the values as integers.
    """
    name_dict = {
        "cross":0,"circle":0,"triangle":0,"sqare":0,
        "l1":0,"l2":0,"r1":0,"r2":0,
        "share":0,"options":0,"PS":0,"l3":0,"r3":0,
        "up":0,"down":0,"right":0,"left":0}
    for key in button_dict.keys():
        if key == 1:
            name_dict["cross"] = bool_to_button(button_dict[key])
        if key == 2:
            name_dict["circle"] = bool_to_button(button_dict[key])
        if key == 0:
            name_dict["square"] = bool_to_button(button_dict[key])
        if key == 3:
            name_dict["triangle"] = bool_to_button(button_dict[key])
        if key == 4:
            name_dict["l1"] = bool_to_button(button_dict[key])
        if key == 5:
            name_dict["r1"] = bool_to_button(button_dict[key])
        if key == 6:
            name_dict["l2"] = bool_to_button(button_dict[key])
        if key == 7:
            name_dict["r2"] = bool_to_button(button_dict[key])
        if key == 4:
            name_dict["share"] = bool_to_button(button_dict[key])
        if key == 6:
            name_dict["options"] = bool_to_button(button_dict[key])
        if key == 5:
            name_dict["PS"] = bool_to_button(button_dict[key])
        if key == 10:
            name_dict["l3"] = bool_to_button(button_dict[key])
        if key == 11:
            name_dict["r3"] = bool_to_button(button_dict[key])

    return name_dict


def bool_to_axis(_bool):
    return int(_bool) * 127


def axis_parser(axis_dict):
    """
    Returns a dict with the names of the axes as keys and the values scaled properly.
    """
    name_dict = {}
    for key in axis_dict.keys():
        if key == 0:
            name_dict["LEFT_STICK_X"] = int(axis_dict[key] * 127)
        if key == 1:
            name_dict["LEFT_STICK_Y"] = -int(axis_dict[key] * 127)
        if key == 2:
            name_dict["RIGHT_STICK_X"] = int(axis_dict[key] * 127)
        if key == 5:
            name_dict["RIGHT_STICK_Y"] = -int(axis_dict[key] * 127)
        if key == 3:
            name_dict["l2"] = int(axis_dict[key] * 64 + 64)
        if key == 4:
            name_dict["r2"] = int(axis_dict[key] * 64 + 64)
    return name_dict

def arrow_parser(hats):
    arr_dict ={"right":0,"left":0,"up":0,"down":0}
    if not hats:
        return arr_dict
    else:
        arr_dict ={"right":1 if hats[0] == 1 else 0,
                   "left":1 if hats[0] == -1 else 0,
                   "up":1 if hats[1] == 1 else 0,
                   "down":1 if hats[1] == -1 else 0}

    return arr_dict



class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()



    def __str__(self):
        steing_to_ret = ''
        for key in self.state_to_print:
            steing_to_ret += key + ':' + str(self.state_to_print[key]) + '\n'
        # steing_to_ret = str(self.state_to_print['LEFT_STICK_X'])
        return steing_to_ret

    def listen(self):
        """Listen for events to happen"""
        self.state_to_print = {
            'LEFT_STICK_X': 0,
            'LEFT_STICK_Y': 0,
            'RIGHT_STICK_X': 0,
            'RIGHT_STICK_Y': 0,
            'SHARE': 0,
            'OPTIONS': 0,
            'PS': 0,
            'UP': 0,
            'RIGHT': 0,
            'DOWN': 0,
            'LEFT': 0,
            'TRIANGLE': 0,
            'CIRCLE': 0,
            'CROSS': 0,
            'SQUARE': 0,
            'L1': 0,
            'R1': 0,
            'L2': 0,
            'R2': 0,
            'L3': 0,
            'R3':0,
        }    

        if not self.axis_data:
            self.axis_data = {1: 0, 0: 0, 5: 0, 2: 0, 3: -1, 4: -1}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = (0,0)
       
        millis = 0

        while True:
            # print(self.state_to_print["L2"],self.state_to_print["R2"],
            #       self.state_to_print["LEFT_STICK_X"],self.state_to_print["LEFT_STICK_Y"],
            #       self.state_to_print["RIGHT_STICK_X"],self.state_to_print["RIGHT_STICK_Y"])
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value, 1)
                elif  event.type ==pygame.JOYHATMOTION:
                    self.hat_data = event.value
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                    # print(event.button)
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                b_dict = parse_button_dict(self.button_data)
                a_dict = axis_parser(self.axis_data)
                ar_dict = arrow_parser(self.hat_data)
                self.state_to_print = {
                    'LEFT_STICK_X': a_dict["LEFT_STICK_X"],
                    'LEFT_STICK_Y': a_dict["LEFT_STICK_Y"],
                    'RIGHT_STICK_X': a_dict["RIGHT_STICK_X"],
                    'RIGHT_STICK_Y': a_dict["RIGHT_STICK_Y"],
                    'SHARE': b_dict['share'],
                    'OPTIONS': b_dict['options'],
                    'PS': b_dict['PS'],
                    'UP': ar_dict['up'],
                    'RIGHT': ar_dict['right'],
                    'DOWN': ar_dict['down'],
                    'LEFT': ar_dict['left'],
                    'TRIANGLE': b_dict['triangle'],
                    'CIRCLE': b_dict['circle'],
                    'CROSS': b_dict['cross'],
                    'SQUARE': b_dict['square'],
                    'L1': b_dict['l1'],
                    'R1': b_dict['r1'],
                    'L2': a_dict['l2'],
                    'R2': a_dict['r2'],
                    'L3': b_dict['l3'],
                    'R3': b_dict['r3'],
                }

    def get_left_stick_pos(self):
        return [self.state_to_print['LEFT_STICK_X'], self.state_to_print['LEFT_STICK_Y']]

    def get_right_stick_pos(self):
        return [self.state_to_print['RIGHT_STICK_X'], self.state_to_print['RIGHT_STICK_Y']]

    def get_buttons(self):
        return [
            self.state_to_print['TRIANGLE']
            , self.state_to_print['CIRCLE']
            , self.state_to_print['CROSS']
            , self.state_to_print['SQUARE']
        ]

    def get_arrows(self):
        return [
            self.state_to_print['UP']
            , self.state_to_print['RIGHT']
            , self.state_to_print['DOWN']
            , self.state_to_print['LEFT']
        ]

    def get_triggers_buttons(self):
        return [
            self.state_to_print['L1']
            , self.state_to_print['L3']
            , self.state_to_print['R1']
            , self.state_to_print['R3']
        ]

    def get_triggers_axis(self):
        return [
            self.state_to_print['L2']
            , self.state_to_print['R2']
        ]


