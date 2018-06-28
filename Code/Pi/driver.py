import RPi.GPIO as GPIO
import time

pins = {'rows': [26, 32, 36, 38, 40],
        'cols': [29, 31, 33, 35, 37]}


def setup():
    GPIO.setmode(GPIO.BOARD)
    for pin in [p for r in pins.values() for p in r]:
        GPIO.setup(pin, GPIO.OUT, GPIO.PUD_OFF, 0)


def tear_down():
    GPIO.cleanup()


def led_toggle(row, col, state):
    row = [int(b) for b in '{0:05b}'.format(row)]
    col = [int(b) for b in '{0:05b}'.format(col+8)]
    for e in zip(row+col, pins['rows']+pins['cols']):
        if e[0]:
            GPIO.output(e[1], state)


def led_lumos(row, col):
    led_toggle(row, col, 1)


def led_off(row, col):
    led_toggle(row, col, 0)


def leds_lumos(leds, delay=.00001):
    for led in leds:
        # print(led)
        led_lumos(*led)
        # time.sleep(delay)
        led_off(*led)


def test1():
    try:
        print('init')
        setup()
        while 1:
            leds = [(i, j) for i in range(10) for j in range(20)]
            leds_lumos(leds, .1)
    finally:
        tear_down()
