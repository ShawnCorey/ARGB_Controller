import serial
import time
import struct
from enum import Enum, auto


ser = serial.Serial('/dev/ttyACM0')
ser.timeout = 2


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
    print(command)
    ser.write(command)
    response = ser.readlines()
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


setLEDLength(ser, 42)
setBrightness(ser, 10)
setDelay(ser, 100)

setEffectBreathe(ser, 255, 0, 255)

# setLEDLength(ser, 9)

# setBrightness(ser, 5)

# setDelay(ser, 64)

# setLEDLength(ser, 42)

# setEffectChase(ser, 1, 0, 0, 255)
# time.sleep(2)

# setEffectChase(ser, 5, 0, 255, 255)
# time.sleep(2)
# setBrightness(ser, 10)

# setEffectSolid(ser, 255, 255, 255)

# setEffectSolid(ser, 0, 0, 255)
# time.sleep(2)
# setEffectSolid(ser, 0, 255, 0)
# time.sleep(2)
# setLEDLength(ser, 18)
# time.sleep(2)
# setEffectSolid(ser, 255, 0, 0)
# time.sleep(2)

# setLEDLength(ser, 42)

# setEffectWipe(ser, 255, 0, 255)
# time.sleep(10)
# setBrightness(ser, 10)
# time.sleep(2)
# setBrightness(ser, 5)

# setEffectRainbow(ser)

# setDelay(ser, 10)

# setLEDLength(ser, 42)
