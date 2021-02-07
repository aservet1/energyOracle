from energy_series import EnergySeries
import matplotlib.pyplot as plt

class Forecaster:
    def __init__(self, start, stop, host, port, db, measurement):
        self.start = start
        self.stop = stop
        self.conn_details = {}
        self.conn_details['host'] = host
        self.conn_details['port'] = port
        self.conn_details['db'] = db
        self.conn_details['measurement'] = measurement
    def setup(self):
        self.train_data = EnergySeries(self.start, self.stop, self.conn_details['host'], self.conn_details['port'], self.conn_details['db'], self.conn_details['measurement']).get_train_data()
    def train(self):
        pass
    def forecast(self):
        pass
    def run(self):
        self.setup()
        print(self.train_data)
        plt.plot(self.train_data["CORE"])
        plt.show()
        self.train()
        self.forecast()
def main():
    f = Forecaster(None, None, 'localhost', 8086, 'Energy_Database', 'energy_readings').run()
main()
