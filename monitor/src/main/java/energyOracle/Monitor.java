/*
	credit to:	https://www.baeldung.com/java-timer-and-timertask
				https://www.baeldung.com/java-influxdb
*/

package energyOracle;

import java.time.Instant;
import java.util.Timer;
import java.util.TimerTask;

import jRAPL.*;

class DbSubmitter extends TimerTask { // is there anywhere that i can do monitor.delloc() in a shutdown() function?

	// discard the first few readings since they can be unreliable
	private static long counter = 0;
	private static final long WARMUP_ITERATIONS = 3; // @TODO MAKE SURE YOU (maybe) SET THIS BACK TO 5 BEFORE YOU ACTUALLY START ENTERING THE DATA!!
	private SyncEnergyMonitor monitor;
	private EnergyStats before, after;
	public DbSubmitter() {
		super();
		monitor = new SyncEnergyMonitor();
		after = monitor.getSample();
		before = after;
	}
	private static void submitToDB(EnergySample es) {
		System.out.println(Utils.toHashMap(es));
	}
	@Override
	public void run() {
		if (counter++ >= WARMUP_ITERATIONS) {
			submitToDB(EnergyDiff.between(before, after));
		}
		else System.out.println("warmup iteration "+counter+"/"+WARMUP_ITERATIONS+" completed");
		before = after;
		after = monitor.getSample();
		// if (cancel == true) cancel();
	}
	public void initEnergyMonitor() { monitor.init(); }
	public void deallocEnergyMonitor() { monitor.dealloc(); }
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
		timer.cancel();
		scheduledTask.deallocEnergyMonitor();
	}

	public static void main(String[] args) throws InterruptedException
	{
		Monitor m = new Monitor();
		System.out.println(Instant.now());
		m.start();
		Thread.sleep(20000);
		m.stop();
	}
}