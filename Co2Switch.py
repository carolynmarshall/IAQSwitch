from m5stack import *
from m5ui import *
from uiflow import *
from base.Socket_Kit import Socket
import time
import unit


co2_0 = unit.get(unit.CO2_SCD40, unit.PORTA)
co2 = None
sock = Socket()

# Toggles the relay state.
#
def maybe_toggle_switch():
  global co2
  if sock.wait_update_data():
    if co2 < 500 and (sock.get_relay_status()):
      sock.set_relay_state(0)
    elif co2 > 600 and not (sock.get_relay_status()):
      sock.set_relay_state(1)

# Sets the colour of the LED based on the CO2 reading.
def set_color():
  global co2
  if co2 < 500:
    rgb.setColorAll(0x99ff99)
  elif co2 < 800:
    rgb.setColorAll(0x33cc00)
  elif co2 < 1000:
    rgb.setColorAll(0xff9900)
  elif co2 < 1200:
    rgb.setColorAll(0xff0000)
  else:
    rgb.setColorAll(0x990000)

sock.set_relay_state(0)
rgb.setColorAll(0xcc33cc)
co2_0.start_periodic_measurement()
wait(5)
while True:
  if co2_0.data_isready():
    co2_0.read_sensor_measurement()
    co2 = co2_0.co2
    set_color()
    maybe_toggle_switch()
  wait_ms(2)
