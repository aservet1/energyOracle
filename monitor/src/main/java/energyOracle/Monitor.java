/*
	credit due to: https://www.baeldung.com/java-timer-and-timertask
*/

package energyOracle;

import java.time.Instant;
import java.util.Timer;
import java.util.TimerTask;

import jRAPL.*;

class DbSubmitter extends TimerTask { // is there anywhere that i can do monitor.delloc() in a shutdown() function?

	// discard the first few readings since they can be unreliable
	private static long counter = 0;
	private static final long WARMUP_ITERATIONS = 5;

	// public boolean cancel = false;

	private SyncEnergyMonitor monitor;
	private EnergyStats before, after;
	public DbSubmitter() {
		super();
		monitor = new SyncEnergyMonitor();
		monitor.init();
		after = monitor.getSample();
		before = after;
	}
	@Override
	public void run() {
		if (counter++ >= WARMUP_ITERATIONS) System.out.println(Utils.toHashMap(EnergyDiff.between(before, after)));
		else System.out.println("warmup iteration "+counter+"/"+WARMUP_ITERATIONS+" completed");
		before = after;
		after = monitor.getSample();
		// if (cancel == true) cancel();
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

	private static void getOnProperInterval(int s) { // catch up to the next 15th second
		while (Instant.now().getEpochSecond() % s != 0);
		System.out.println(Instant.now());
	}

	public void start() {
		getOnProperInterval(15);
		long period = samplingRate;// 1000L * 60L * 60L * 24L;
		timer.scheduleAtFixedRate(scheduledTask, 0, period);
	}

	public void stop() {
		timer.cancel();
	}

	public static void main(String[] args) throws InterruptedException
	{
		Monitor m = new Monitor();
		m.start();
		Thread.sleep(5000);
		m.stop();
	}
}