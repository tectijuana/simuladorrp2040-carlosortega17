# Autor: Carlos Eduardo Ortega Frias
import utime
from machine import Pin, SPI
import max7219

spi = SPI(0, baudrate=1000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)

display = max7219.Matrix8x8(spi, ss, 4)
display.brightness(1)

while True:
  display.text('1', 0, 0, 1)
  display.show()
  utime.sleep(0.3)
  display.fill(0)