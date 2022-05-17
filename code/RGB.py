import time
import board
import adafruit_rgbled

led = adafruit_rgbled.RGBLED(board.GP2, board.GP4, board.GP3, invert_pwm=True)

while True:
  print("Red")
  led.color = (255, 0, 0)
  time.sleep(1)
  print("Blue")
  led.color = (0, 255, 0)
  time.sleep(1)
  print("Green")
  led.color = (0, 0, 255)
  time.sleep(1)