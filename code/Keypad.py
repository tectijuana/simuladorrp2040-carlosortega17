# Autor: Carlos Eduardo Ortega Frias
import utime
from machine import Pin

matrix_keys = [['1','2','3','A'],
['4','5','6','B'],
['7','8','9','C'],
['*','0','#','D']]

keypad_rows = [9,8,7,6]
keypad_columns = [5,4,3,2]

col_pins = []
row_pins = []

for i in range(0,4):
  row_pins.append(Pin(keypad_rows[i], Pin.OUT))
  row_pins[i].value(1)
  col_pins.append(Pin(keypad_columns[i], Pin.IN, Pin.PULL_DOWN))
  col_pins[i].value(0)

print("Please enter key")

def scankeys():
  for row in range(4):
    for col in range(4):
      row_pins[row].high()
      key = None
      if col_pins[col].value() == 1:
        print("You hace pressed: ", matrix_keys[row][col])
        utime.sleep(0.3)
    row_pins[row].low()

while True:
  scankeys()