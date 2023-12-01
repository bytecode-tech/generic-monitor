import os
import importlib
from fastapi import FastAPI

app = FastAPI()

def load_sensor_readers(directory):
    readers = {}
    package = directory.replace('/', '.')
    for filename in os.listdir(directory):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            module = importlib.import_module(f"{package}.{module_name}")
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if isinstance(attribute, type) and hasattr(attribute, 'read'):
                    readers[attribute_name] = attribute()
    return readers

readers = load_sensor_readers('readers')

@app.get("/read_all")
def read_all():
    all_data = {}
    for reader_name, reader in readers.items():
        try:
            data = reader.read()
            if data:
                all_data[reader_name] = data
        except Exception as e:
            all_data[reader_name] = {"error": str(e)}
    return all_data

