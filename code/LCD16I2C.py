import board
import time
import busio
import lcd
import i2c_pcf8574_interface
import digitalio

i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
address = 0x3F


i2c = i2c_pcf8574_interface.I2CPCF8574Interface(i2c, address)

display = lcd.LCD(i2c, num_rows=2, num_cols=16)

display.set_backlight(True)

display.set_display_enabled(True)

display.clear()
display.print("Welcome")