from influxdb import InfluxDBClient
import datetime

class InfluxConnection:
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
        params = {"measurement": measurement}
        result = self.client.query('SELECT * FROM $measurement ORDER BY time DESC LIMIT 1', bind_params=params)
        return result
    def get_readings(self, start, stop, measurement):
        params = {"measurement": measurement}
        query = ["SELECT * FROM ", measurement]
        if start:
            params["start"] = start.strftime("%Y-%m-%d %H-%M-%S")
            query.append(" where time >= $start")
        if stop:
            params["stop"] = stop.strftime("%Y-%m-%d %H-%M-%S")
            if start:
                query.append(" and ")
            else:
                query.append(" where ")
            query.append("time <= $stop")
        return self.client.query("".join(query))

def main():
    conn = InfluxConnection('localhost', 8086, 'Energy')
    # for row in conn.get_last_reading('energy').get_points():
    #     print(row)
    # for row in get_last_reading
    print(conn.get_readings(datetime.datetime.fromtimestamp(1612645058182219610), None, "yay"))
        
main()