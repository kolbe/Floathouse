# An Accessory for a LED attached to pin 11.
import logging

import RPi.GPIO as GPIO
import time

from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_LIGHTBULB



class LightBulb(Accessory):

    category = CATEGORY_LIGHTBULB

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        serv_light = self.add_preload_service('Lightbulb')
        self.char_on = serv_light.configure_char(
            'On', setter_callback=self.set_bulb)

    '''
    def __setstate__(self, state):
        self.__dict__.update(state)
        self._gpio_setup(self.pin)
    '''

    def execCmd(self, cmd):
        if cmd == "on":
            pin = 17
        elif cmd== "off":
            pin = 18
        else:
            print("Command '{}' is invalid.".format(cmd))
            return

        GPIO.setup(pin,GPIO.OUT)
        #print "'{}' button press".format(cmd)
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(0.2)
        #print "'{}' button release".format(cmd)
        GPIO.output(pin,GPIO.LOW)
    def set_bulb(self, value):
        if value:
            self.execCmd('on')
        else:
            self.execCmd('off')

    def stop(self):
        super().stop()
        GPIO.cleanup()
