# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 matt
#
# SPDX-License-Identifier: MIT
"""
`roberts_usb`
================================================================================

Turns Robers Radio Controls in to USB HID device


* Author(s): matt

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s).
  Use unordered list & hyperlink rST inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies
  based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/zenbandit1/CircuitPython_Roberts_usb.git"

import board
import time
import usb_hid
from digitalio import DigitalInOut, Direction, Pull
from rotaryio import IncrementalEncoder
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.consumer_control import ConsumerControl

kbd = Keyboard(usb_hid.devices)

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True #dat

# Change the below code for different outcomes
# https://circuitpython.readthedocs.io/projects/hid/en/latest/

# Button Press will mute
BUTTON_CODE = (Keycode.C)
BUTTON_CODE1 = (Keycode.B)
BUTTON_CODE2 = (Keycode.A)
BUTTON_CODE3 = (Keycode.D)
BUTTON_CODE4 = (Keycode.E)
BUTTON_CODE5 = (Keycode.F)
BUTTON_CODE6 = (Keycode.G)
BUTTON_CODE7= (Keycode.H)
# Rotating the encoder clockwise will increase the volume
INCREMENT_CODE = ConsumerControlCode.VOLUME_DECREMENT
INCREMENT_CODE_PRESSED = ConsumerControlCode.REWIND
INCREMENT_CODE1 = (Keycode.UP_ARROW)
INCREMENT_CODE_PRESSED1 = (Keycode.UP_ARROW)
INCREMENT_CODE2 = (Keycode.LEFT_ARROW)
INCREMENT_CODE_PRESSED2 = (Keycode.LEFT_ARROW)
#INCREMENT_CODE = (Keycode.UP_ARROW)
# Press ctrl-x.
#kbd.press(Keycode.LEFT_CONTROL, Keycode.X)
# Rotating the encoder clockwise will decrease teh volume
DECREMENT_CODE = ConsumerControlCode.VOLUME_INCREMENT
DECREMENT_CODE_PRESSED = ConsumerControlCode.FAST_FORWARD
DECREMENT_CODE1 = (Keycode.DOWN_ARROW)
DECREMENT_CODE_PRESSED1 = (Keycode.DOWN_ARROW)
DECREMENT_CODE2 = (Keycode.RIGHT_ARROW)
DECREMENT_CODE_PRESSED2 = (Keycode.RIGHT_ARROW)
# initialize as hid device
consumer_control = ConsumerControl(usb_hid.devices)

# initialize encoder on pins D0 and D1 (QT Py M0)
encoder = IncrementalEncoder(board.GP0, board.GP1) # not used
encoder1 = IncrementalEncoder(board.GP20, board.GP21) # tuning button
encoder2 = IncrementalEncoder(board.GP4, board.GP5) # 'volume' button
# initialize encoder click on pin D2 (QT Py M0)
button = DigitalInOut(board.GP17) #Tuning button
button.direction = Direction.INPUT
button.pull = Pull.UP
button1 = DigitalInOut(board.GP16) #eset button keybd
button1.direction = Direction.INPUT
button1.pull = Pull.UP
button2 = DigitalInOut(board.GP9) #info button
button2.direction = Direction.INPUT
button2.pull = Pull.UP
button3 = DigitalInOut(board.GP8) #auto tune button
button3.direction = Direction.INPUT
button3.pull = Pull.UP
button4 = DigitalInOut(board.GP6) #fm/dab button
button4.direction = Direction.INPUT
button4.pull = Pull.UP
button5 = DigitalInOut(board.GP2) #'volume' button
button5.direction = Direction.INPUT
button5.pull = Pull.UP
button6 = DigitalInOut(board.GP13) #favourite button
button6.direction = Direction.INPUT
button6.pull = Pull.UP
button7 = DigitalInOut(board.GP3) # not used
button7.direction = Direction.INPUT
button7.pull = Pull.UP

button_in = False
button_in1 = False
button_in2 = False
button_in3 = False
last_position = None
last_position1 = None
last_position2 = None

while True:

    if not button.value and not button_in:
        print("button press")
        button_in = True
        kbd.send(BUTTON_CODE)
        time.sleep(.2)

    elif button.value and button_in:
        button_in = False
        
    elif not button.value and button_in:
        position = encoder.position

        if last_position is not None and position != last_position:

            if position > last_position:
                print("rotate clockwise-pressed")
                consumer_control.send(INCREMENT_CODE_PRESSED)

            elif position < last_position:
                print("rotate counter-clockwise-pressed")
                consumer_control.send(DECREMENT_CODE_PRESSED)

        last_position = position

    elif button.value and not button_in:
        position = encoder.position

        if last_position is not None and position != last_position:

            if position > last_position:
                print("rotate clockwise")
                consumer_control.send(INCREMENT_CODE)

            elif position < last_position:
                print("rotate counter-clockwise")
                consumer_control.send(DECREMENT_CODE)

        last_position = position
        
    if not button1.value and not button_in1:
        print("button1 press")
        button_in1 = True
        kbd.send(BUTTON_CODE1)
        
        time.sleep(.2)
        
    elif button1.value and button_in1:
        button_in1 = False


    elif not button1.value and button_in1:
        position1 = encoder1.position
        if last_position1 is not None and position1 != last_position1:

            if position1 > last_position1:
                print("rotate clockwise-pressed1")
                kbd.send(INCREMENT_CODE_PRESSED1)

            elif position1 < last_position1:
                print("rotate counter-clockwise-pressed1")
                kbd.send(DECREMENT_CODE_PRESSED1)

        last_position1 = position1

    elif button1.value and not button_in1:
        position1 = encoder1.position

        if last_position1 is not None and position1 != last_position1:

            if position1 > last_position1:
                print("rotate clockwise1")
                kbd.send(INCREMENT_CODE1)

            elif position1 < last_position1:
                print("rotate counter-clockwise1")
                kbd.send(DECREMENT_CODE1)

        last_position1 = position1
        

    if not button2.value and not button_in2:
            print("button2 press")
            button_in2 = True
            kbd.press(BUTTON_CODE2)
            time.sleep(0.2)
            kbd.release(BUTTON_CODE2)
            #time.sleep(.2)aaaaaaaaaaaaaaaaaaaaaaaaaaa
            
            
    elif button2.value and button_in2:
            button_in2 = False

    elif not button2.value and button_in2:
        position2 = encoder2.position

        if last_position2 is not None and position2 != last_position2:

             if position2 > last_position2:
                    print("rotate clockwise-pressed2")
                    kbd.send(INCREMENT_CODE_PRESSED2)

             elif position2 < last_position2:
                    print("rotate counter-clockwise-pressed2")
                    kbd.send(DECREMENT_CODE_PRESSED2)

        last_position2 = position2

    elif button2.value and not button_in2:
        position2 = encoder2.position
            
        if last_position2 is not None and position2 != last_position2:

            if position2 > last_position2:
                    print("rotate clockwise2")
                    kbd.send(INCREMENT_CODE2)

            elif position2 < last_position2:
                    print("rotate counter-clockwise2")
                    kbd.send(DECREMENT_CODE2)

        last_position2 = position2

    if not button3.value:
            print("button3 press")
            kbd.send(BUTTON_CODE3)
            time.sleep(.2)
            
    if not button4.value:
            print("button4 press")
            kbd.send(BUTTON_CODE4)
            time.sleep(.2)

    if not button5.value:
            print("button5 press")
            kbd.send(BUTTON_CODE5)
            time.sleep(.2)
            
    if not button6.value:
            print("button6 press")
            kbd.send(BUTTON_CODE6)
            time.sleep(.2)
            
    if not button7.value:
            print("button7 press")
            kbd.send(BUTTON_CODE7)
            time.sleep(.2)
