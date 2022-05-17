import board
import time
import analogio

meter = analogio.AnalogIn(board.GP28)

while True:
  print(meter.value)
  time.sleep(0.1)