import serial
import time
import struct
from enum import Enum, auto
import argparse


# ser = serial.Serial('/dev/ttyACM0')
# ser.timeout = 2


class Settings(Enum):
    Brightness = 0
    Delay = 1
    Length = 2


class Effects(Enum):
    Solid = 0
    Rainbow = 1
    Chase = 2
    Wipe = 3
    Breathe = 4


def sendCommand(serial, command):
    # print(command)
    ser.write(command)
    response = ser.readline()
    for line in response:
        print(line)


def setLEDLength(ser, numLEDs):
    val = struct.pack('>H', numLEDs)
    setting = struct.pack('B', Settings.Length.value)
    sendCommand(ser, b'S' + setting + val)


def setBrightness(ser, brightness):
    val = struct.pack('B', brightness)
    setting = struct.pack('B', Settings.Brightness.value)
    sendCommand(ser, b'S' + setting + val)


def setDelay(ser, delay):
    val = struct.pack('B', delay)
    setting = struct.pack('B', Settings.Delay.value)
    sendCommand(ser, b'S' + setting + val)


def setEffect(ser, effect, options=b''):
    sendCommand(ser, effect + options)


def setEffectRainbow(ser):
    effect = struct.pack('B', Effects.Rainbow.value)
    setEffect(ser, b'E' + effect)


def setEffectChase(ser, length, R, G, B):
    effect = struct.pack('B', Effects.Chase.value)
    encLength = struct.pack('B', length)
    encR = struct.pack('B', R)
    encG = struct.pack('B', G)
    encB = struct.pack('B', B)
    setEffect(ser, b'E' + effect + encR + encG + encB + encLength)


def setEffectSolid(ser, R, G, B):
    effect = struct.pack('B', Effects.Solid.value)
    encR = struct.pack('B', R)
    encG = struct.pack('B', G)
    encB = struct.pack('B', B)
    setEffect(ser, b'E' + effect + encR + encG + encB)


def setEffectWipe(ser, R, G, B):
    effect = struct.pack('B', Effects.Wipe.value)
    encR = struct.pack('B', R)
    encG = struct.pack('B', G)
    encB = struct.pack('B', B)
    setEffect(ser, b'E' + effect + encR + encG + encB)

def setEffectBreathe(ser, R, G, B):
    effect = struct.pack('B', Effects.Breathe.value)
    encR = struct.pack('B', R)
    encG = struct.pack('B', G)
    encB = struct.pack('B', B)
    setEffect(ser, b'E' + effect + encR + encG + encB)


parser = argparse.ArgumentParser()

parser.add_argument('-s', '--serial-port', help='Set serial port to use', required=True)

parser.add_argument('-e', '--effect', choices=['solid','rainbow','chase','wipe','breathe'],
                    help='Set lighting effect', required=False)

parser.add_argument('--chase-length', type=int, help='Set the length for the chase effect', required=False)


parser.add_argument('-c', '--color', nargs=3, type=int,
                    help='Set the color for the related effect use "-c <R> <G> <B>"', required=False)

parser.add_argument('-b', '--brightness', type=int, help='Set the brightness', required=False)

parser.add_argument('-d', '--delay', type=int, help='Set the effect delay', required=False)

parser.add_argument('-l', '--length', type=int, help='Set the LED string length', required=False)

args = parser.parse_args()

ser = serial.Serial(args.serial_port)
ser.timeout = 1

if args.delay != None:
    setDelay(ser, args.delay)

if args.brightness != None:
    setBrightness(ser, args.brightness)

if args.length != None:
    setLEDLength(ser, args.length)

if args.effect != None:
    if args.effect == "rainbow":
        setEffectRainbow(ser)
    if args.effect == "solid":
        if args.color == None:
            print("Color required!")
            exit(-1)
        setEffectSolid(ser, args.color[0], args.color[1], args.color[2])
    if args.effect == "chase":
        if args.color == None or args.chase_length == None:
            print("Color and Chase Length required!")
            exit(-1)
        setEffectChase(ser, args.chase_length, args.color[0], args.color[1], args.color[2])
    if args.effect == "wipe":
        if args.color == None:
            print("Color required!")
            exit(-1)
        setEffectWipe(ser, args.color[0], args.color[1], args.color[2])
    if args.effect == "breathe":
        if args.color == None:
            print("Color required!")
            exit(-1)
        setEffectBreathe(ser, args.color[0], args.color[1], args.color[2])