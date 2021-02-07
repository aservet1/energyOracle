package energyOracle;

import java.time.Instant;
import java.util.concurrent.TimeUnit;

import org.influxdb.InfluxDB;
import org.influxdb.InfluxDBFactory;
import org.influxdb.dto.Point;
import org.influxdb.dto.Pong;

public class DBTest {
    public static void main(String... args) {
        String dbName = "testSample";

        InfluxDB influxDB = InfluxDBFactory.connect("http://localhost:8086");
        Pong response = influxDB.ping();
        if (response.getVersion().equalsIgnoreCase("unknown")) {
            System.err.println("Error pinging server.");
            System.exit(1);
        }

        influxDB.createDatabase(dbName);
        influxDB.createRetentionPolicy("defaultPolicy", dbName, "30d", 1, true);
        influxDB.setLogLevel(InfluxDB.LogLevel.BASIC);

        influxDB.enableBatch(100, 200, TimeUnit.MILLISECONDS);
        influxDB.setRetentionPolicy("defaultPolicy");
        influxDB.setDatabase(dbName);
        // 



        Point point = Point.measurement("memory")
            .time(Instant.now().getEpochSecond(), TimeUnit.SECONDS)
            .addField("name", "server1")
            .addField("free", 4743656L)
            .addField("used", 1015096L)
            .addField("buffer", 1010467L)
            .build();

        influxDB.write(point);

        influxDB.disableBatch();

        influxDB.close();
    }
}
