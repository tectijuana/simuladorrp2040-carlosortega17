import time
import board
import analogio
import adafruit_thermistor

thermistor = adafruit_thermistor.Thermistor(board.GP28, 10000.0, 10000.0, 25.0, 3950.0, high_side=False)

while True:
  celcius = thermistor.temperature
  print(celcius)
  time.sleep(0.1)