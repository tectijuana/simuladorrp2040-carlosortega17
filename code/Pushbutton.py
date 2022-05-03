# Autor: Carlos Eduardo Ortega Frias
import time
import board
import digitalio

button = digitalio.DigitalInOut(board.GP13)
button.switch_to_input(pull=digitalio.Pull.DOWN)
led = digitalio.DigitalInOut(board.GP14)
led.direction = digitalio.Direction.OUTPUT

while True:
  print(button.value)
  if button.value:
    led.value = True
  else:
    led.value = False
  time.sleep(0.5)