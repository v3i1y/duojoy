import pygame

"""
Dual Shock Joy Stick Mappings
"""
BUTTON_CROSS = 0
BUTTON_CIRCLE = 1
BUTTON_SQUARE = 2
BUTTON_TRIANGLE = 3
BUTTON_OPTIONS = 6
BUTTON_L3 = 7
BUTTON_R3 = 8
BUTTON_L1 = 9
BUTTON_R1 = 10
BUTTON_UP = 11
BUTTON_DOWN = 12
BUTTON_LEFT = 13
BUTTON_RIGHT = 14
BUTTON_MIDDLE_PAD = 15
AXIS_LEFT_STICK_LEFT_RIGHT = 0
AXIS_LEFT_STICK_UP_DOWN = 1
AXIS_RIGHT_STICK_LEFT_RIGHT = 2
AXIS_RIGHT_STICK_UP_DOWN = 3
AXIS_L2 = 4
AXIS_R2 = 5

"""
VJOY Genshin Mapping
"""
VJOY_SQUARE = 1
VJOY_CROSS = 2
VJOY_CIRCLE = 3
VJOY_TRIANGLE = 4
VJOY_L1 = 5
VJOY_R1 = 6
VJOY_L2 = 7
VJOY_R2 = 8
VJOY_OPTIONS = 10
VJOY_L3 = 11
VJOY_R3 = 12
VJOY_MIDDLE_PAD = 14

VJOY_DPAD_UP    = 0
VJOY_DPAD_RIGHT = 1
VJOY_DPAD_DOWN  = 2
VJOY_DPAD_LEFT  = 3

VJOY_INPUT_TYPE_BUTTON = 0
VJOY_INPUT_TYPE_AXIS   = 1
VJOY_INPUT_TYPE_POV    = 2

HID_USAGE_X   = 0x30
HID_USAGE_Y	  = 0x31
HID_USAGE_Z	  = 0x32
HID_USAGE_RX  = 0x33
HID_USAGE_RY  = 0x34
HID_USAGE_RZ  = 0x35
HID_USAGE_SL0 = 0x36
HID_USAGE_SL1 = 0x37
HID_USAGE_WHL = 0x38
HID_USAGE_POV = 0x39

def map_event(event):
    # global l1_pressed
    # global paused

    if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
        vjoy_type   = VJOY_INPUT_TYPE_BUTTON 
        vjoy_axis   = None
        vjoy_value  = 1 if event.type == pygame.JOYBUTTONDOWN else 0

        button = event.button
        if button == BUTTON_CROSS:
            vjoy_axis = VJOY_CROSS
        elif button == BUTTON_CIRCLE:
            vjoy_axis = VJOY_CIRCLE
        elif button == BUTTON_SQUARE:
            vjoy_axis = VJOY_SQUARE
        elif button == BUTTON_TRIANGLE:
            vjoy_axis = VJOY_TRIANGLE
        elif button == BUTTON_OPTIONS:
            vjoy_axis = VJOY_OPTIONS
        elif button == BUTTON_L1:
            # l1_pressed = True if vjoy_value == 1 else False
            vjoy_axis = VJOY_L1
        elif button == BUTTON_R1:
            # if l1_pressed and vjoy_value == 1:
            #     print('paused', paused)
            #     paused += 1
            vjoy_axis = VJOY_R1
        elif button == BUTTON_UP:
            vjoy_type = VJOY_INPUT_TYPE_POV
            vjoy_axis = VJOY_DPAD_UP
        elif button == BUTTON_DOWN:
            vjoy_type = VJOY_INPUT_TYPE_POV
            vjoy_axis = VJOY_DPAD_DOWN
        elif button == BUTTON_LEFT:
            vjoy_type = VJOY_INPUT_TYPE_POV
            vjoy_axis = VJOY_DPAD_LEFT
        elif button == BUTTON_RIGHT:
            vjoy_type = VJOY_INPUT_TYPE_POV
            vjoy_axis = VJOY_DPAD_RIGHT
        elif button == BUTTON_MIDDLE_PAD:
            vjoy_axis = VJOY_MIDDLE_PAD
        elif button == BUTTON_L3:
            vjoy_axis = VJOY_L3
        elif button == BUTTON_R3:
            vjoy_axis = VJOY_R3
        if vjoy_axis == None:
            return None
        
        return vjoy_type, vjoy_axis, vjoy_value

    if event.type == pygame.JOYAXISMOTION:
        if event.axis == AXIS_L2 or event.axis == AXIS_R2:
            vjoy_type  = VJOY_INPUT_TYPE_BUTTON
            vjoy_axis  = VJOY_R2 if event.axis == AXIS_R2 else VJOY_L2
            vjoy_value = 1 if event.value > 0 else 0
            return vjoy_type, vjoy_axis, vjoy_value

        vjoy_type = VJOY_INPUT_TYPE_AXIS
        if event.axis == AXIS_RIGHT_STICK_LEFT_RIGHT:
            vjoy_axis = HID_USAGE_Z
        elif event.axis == AXIS_RIGHT_STICK_UP_DOWN:
            vjoy_axis = HID_USAGE_RZ
        elif event.axis == AXIS_LEFT_STICK_LEFT_RIGHT:
            vjoy_axis = HID_USAGE_X
        elif event.axis == AXIS_LEFT_STICK_UP_DOWN:
            vjoy_axis = HID_USAGE_Y
        else:
            return None

        vjoy_value = 0.5 + event.value / 2
        vjoy_value = max(vjoy_value, 0)
        vjoy_value = min(vjoy_value, 1)
        vjoy_value *= 0x8000

        return vjoy_type, vjoy_axis, vjoy_value
    return None