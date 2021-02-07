from influxdb import InfluxDBClient
import datetime

class InfluxDBConnection:
    def __init__(self, host, port, db):
        self.client = InfluxDBClient(host=host, port=port)
        found = False
        for db_ in self.client.get_list_database():
            if db_["name"] == db:
                found = True
                break
        if not found:
            self.client.create_database(db)
        self.client.switch_database(db)

    def get_last_reading(self, measurement):
        result = self.client.query(f'SELECT * FROM {measurement} ORDER BY time DESC LIMIT 1')
        return result

    def get_readings(self, start, stop, measurement, limit=None):
        params = {"measurement": measurement}
        query = ["SELECT * FROM ", measurement]
        if start:
            params["start"] = start.strftime("%Y-%m-%d %H:%M:%S")
            query.append(" where time >= $start")
        if stop:
            params["stop"] = stop.strftime("%Y-%m-%d %H:%M:%S")
            if start:
                query.append(" and ")
            else:
                query.append(" where ")
            query.append("time <= $stop")
        query.append(" ORDER BY time")
        if limit is not None:
            query.append(f" LIMIT {limit}")
        return self.client.query("".join(query), bind_params=params)

    def insert_from_file(self, fname, measurement):
        keys = [("DRAM",1), ("GPU", 2), ("PKG", 4), ("CORE", 3)]
        points = []
        with open("sampleOut.txt") as fh:
            for line_num, line in enumerate(fh):
                if line_num < 2:
                    continue
                data = line.split(',')
                data_dict = {}
                data_dict["fields"] = {}
                data_dict["tags"] = {}
                data_dict["tags"]["socket"] = int(data[0])
                for key in keys:
                    data_dict["fields"][key[0]] = float(data[key[1]])
                data_dict["time"] = datetime.datetime.fromtimestamp(int(float(data[6]))).strftime("%Y-%m-%d %H:%M:%S")
                data_dict["measurement"] = measurement
                points.append(data_dict)
        self.client.write_points(points)

    def write_df_to_db(self, df, measurement):
        data = {}
        
    def close(self):
        self.client.close()