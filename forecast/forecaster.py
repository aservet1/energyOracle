from forecast.energy_series import EnergySeries
import matplotlib.pyplot as plt
import pandas as pd
from fbprophet import Prophet

class Forecaster:

    def __init__(self, start, stop, host, port, db, measurement):
        self.start = start
        self.stop = stop
        self.conn_details = {}
        self.conn_details['host'] = host
        self.conn_details['port'] = port
        self.conn_details['db'] = db
        self.conn_details['measurement'] = measurement
        self.hyperparameters = {"daily_seasonality":True} # "seasonality_prior_scale":10 , "changepoint_prior_scale": 0.3, "changepoint_prior_scale": 0.03, "changepoint_range": 0.70
    
    def setup(self):
        self.train_data = EnergySeries(self.start, self.stop, self.conn_details['host'], self.conn_details['port'], self.conn_details['db'], self.conn_details['measurement']).get_train_data()
        self.train_data.pop('socket')
        self.train_data.set_index('ds', inplace=True)
        self.train_data = self.train_data.rolling(10).mean()
    
    def train(self):
        self.training_sets = {}
        self.models = {}
        for column in {"DRAM", "GPU", "PKG", "CORE"}:
            training_set = pd.DataFrame(self.train_data[column])
            training_set.rename(columns={column: "y"}, inplace=True)
            training_set.reset_index(inplace=True)
            self.training_sets[column] = training_set
            m = Prophet(**self.hyperparameters)
            #m = Prophet()
            m.fit(training_set )
            self.models[column] = m

    def forecast(self):
        self.forecasts = {}
        n = len(self.train_data)/2
        for domain in self.models:
            m = self.models[domain]
            future = m.make_future_dataframe(periods=1100, freq='15s')
            self.forecasts[domain] = m.predict(future)

    def run(self):
        self.setup()
        self.train()
        self.forecast()

def main():
    f = Forecaster(None, None, 'localhost', 8086, 'energyDB', 'energy')
    f.run()
    for col in {"DRAM", "GPU", "PKG", "CORE"}:
        print(f.train_data.columns)
        print(f.forecasts[col].columns)

        plt.plot(f.training_sets[col]['ds'], f.training_sets[col]['y'])
        plt.plot( f.forecasts[col]['ds'], f.forecasts[col]['yhat'])
        plt.show()

main()
