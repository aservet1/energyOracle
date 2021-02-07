/*
	credit to:	https://www.baeldung.com/java-timer-and-timertask
				https://www.baeldung.com/java-influxdb
*/

package energyOracle;

import java.util.HashMap;

import java.time.Instant;
import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.TimeUnit;

import org.influxdb.InfluxDB;
import org.influxdb.InfluxDBFactory;
import org.influxdb.dto.Point;
import org.influxdb.dto.Pong;

import jRAPL.*;

class DbSubmitter extends TimerTask { // is there anywhere that i can do monitor.delloc() in a shutdown() function?

	// discard the first few readings since they can be unreliable
	private static long counter = 0;
	private static final long WARMUP_ITERATIONS = 3; // @TODO MAKE SURE YOU (definitelyinfu) SET THIS BACK TO 3 BEFORE YOU ACTUALLY START ENTERING THE DATA!!
	private static final String DB_NAME = "energyDB"; // @TODO MAKE SURE IT'S THE CORRECT NAME BY THE TIME YOU START YOUR LONG TERM ENERGY STORAGE	
	private SyncEnergyMonitor monitor;
	private EnergyStats before, after;
	InfluxDB db;
	public DbSubmitter() {
		super();
		db = createInfluxDB(DB_NAME);
		monitor = new SyncEnergyMonitor();
	}
	private InfluxDB createInfluxDB(String dbName) {	
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
		return influxDB;
	}
	// public static HashMap<String, HashMap<String,Double>> toHashMap(EnergySample energy) {
    //     HashMap<String, HashMap<String,Double>> M = new HashMap<String,HashMap<String,Double>>();
    //     for (int socket = 1; socket <= ArchSpec.NUM_SOCKETS; socket++) {
    //         HashMap<String,Double> m = new HashMap<String,Double>();
    //         m.put("DRAM", energy.atSocket(socket).getDram());
    //         m.put("GPU", energy.atSocket(socket).getGpu());
    //         m.put("CORE", energy.atSocket(socket).getCore());
    //         m.put("PKG", energy.atSocket(socket).getPackage());
    //         // m.put("timestamp", (double)Instant.now().getEpochSecond());
    //         M.put("Socket"+socket,m);
    //     }
    //     // m.put("timestamp", Math.floor((double)Instant.now().getEpochSecond()),);
    //     return M;
    // }
	private void submitToDB(EnergySample es) {
		System.out.println("((("+es.dump());
		for (int socket = 1; socket <= ArchSpec.NUM_SOCKETS; socket++) {
			Point point = Point.measurement("energy")
				.time(Instant.now().getEpochSecond(), TimeUnit.SECONDS)
				.addField("DRAM", es.atSocket(socket).getDram())
				.addField("CORE", es.atSocket(socket).getCore())
				.addField("GPU", es.atSocket(socket).getGpu())
				.addField("PKG", es.atSocket(socket).getPackage())
				.addField/*Tag*/("socket", socket)
				.build();
			db.write(point);
		}
	}
	@Override
	public void run() {
		if (counter++ >= WARMUP_ITERATIONS) {
			submitToDB(EnergyDiff.between(before, after));
		}
		else {
			System.out.println("warmup iteration "+counter+"/"+WARMUP_ITERATIONS+" completed -- " + Instant.now());
		}
		before = after;
		after = monitor.getSample();
	} 
	public void initEnergyMonitor() { 
		monitor.init();
		after = monitor.getSample();
		before = after;
	} 
	public void deallocEnergyMonitor() {
		monitor.dealloc();
	} 
}

public class Monitor
{
	private long samplingRate;
	DbSubmitter scheduledTask;
	Timer timer;

	public Monitor() {
		samplingRate = 15000L; // default every 15 seconds
		scheduledTask = new DbSubmitter();
		timer = new Timer("Timer");
	}

	private static void getOnProperInterval(long ms) { // catch up to the next 15th second
		long sec = ms / 1000;
		while (Instant.now().getEpochSecond() % sec != 0);
		System.out.println(Instant.now());
	}

	public void start() {
		scheduledTask.initEnergyMonitor();
		getOnProperInterval(samplingRate);
		long period = samplingRate;
		timer.scheduleAtFixedRate(scheduledTask, 0, period);
	}

	public void stop() {
		System.out.println("stopping");
		System.exit(0);
		// System.out.println("flag");
		// timer.cancel();
		// System.out.println("flag");
		// scheduledTask.deallocEnergyMonitor();
		// return;
	}

	public static void main(String[] args) throws InterruptedException
	{
		Monitor m = new Monitor();
		System.out.println(Instant.now());
		m.start();
		Thread.sleep(120000);
		m.stop();
	}
}
