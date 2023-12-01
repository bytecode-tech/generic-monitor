# w1_temp_reader.py
import glob
import time

class W1TempReader:
    base_dir = '/sys/bus/w1/devices/'
    
    def __init__(self, device_id=None):
        if device_id:
            self.device_folder = f"{self.base_dir}{device_id}"
        else:
            self.device_folder = glob.glob(self.base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'

    def read_temp_raw(self):
        with open(self.device_file, 'r') as f:
            return f.readlines()

    def read(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return {"w1_temp_celsius": temp_c, "w1_temp_fahrenheit": temp_f}

    @staticmethod
    def get_device_ids():
        device_folders = glob.glob(W1TempReader.base_dir + '28*')
        return [folder.split('/')[-1] for folder in device_folders]
