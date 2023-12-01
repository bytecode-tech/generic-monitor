# sht3x_reader.py
import logging
import board
import busio
import adafruit_sht31d

_LOGGER = logging.getLogger(__name__)

class SHT3xReader:
    def __init__(self):
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.sensor = adafruit_sht31d.SHT31D(i2c)
            self.sensor.frequency = adafruit_sht31d.FREQUENCY_2
            self.sensor.mode = adafruit_sht31d.MODE_PERIODIC
        except:
            _LOGGER.exception("SHT-30 not initialized")

    def read(self):
        try:
            fTemp = (1.8 * self.sensor.temperature[0]) + 32
            humidity = self.sensor.relative_humidity[0]
            return {"sht3x_temperature": fTemp, "sht3x_humidity": humidity}
        except:
            _LOGGER.error("SHT-30 not reporting")

