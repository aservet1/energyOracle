import fbprophet as Prophet
import pandas as pd

class Forecast:
    def __init__(self, timeseries):
        self.model = Prophet()
        self.model.fit(timeseries)

    def model_from_params(cls, params, timeseries):
        self.model = 