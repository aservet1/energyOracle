import pandas as pd
from influx_connection import InfluxDBConnection
from datetime import datetime

class EnergySeries:
    def __init__(self, start, stop, host, port, db, measurement):
        conn = InfluxDBConnection(host, port, db)
        for readings in conn.get_readings(start, stop, measurement):
            for reading in readings:
                reading["time"] = datetime.strptime(reading["time"], "%Y-%m-%dT%H:%M:%SZ")
            self.df = pd.DataFrame(readings)
        conn.close()
        
    def get_train_data(self):
        self.df.rename(columns={"time": "ds"}, inplace=True)
        self.df.set_index('ds')
        return self.df
