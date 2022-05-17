import time
import board
import pwmio
import servo

pwm = pwmio.PWMOut(board.GP5, duty_cycle=2 ** 15, frequency=50)

servo1 = servo.Servo(pwm)

while True:
  for angle in range(0, 180, 5):
    servo1.angle = angle
    time.sleep(0.5)
  for angle in range(180, 0, -5):
    servo1.angle = angle
    time.sleep(0.5)