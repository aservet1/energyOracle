package energyOracle;


/*
	credit due to: https://www.baeldung.com/java-timer-and-timertask

*/

import java.time.Instant;
import java.util.Timer;
import java.util.TimerTask;

import jRAPL.*;

class DbSubmit extends TimerTask {
	private static SyncEnergyMonitor monitor;
	private static EnergyStats before, after;
	static {
		monitor.init();
		after = monitor.getSample();
	}
	@Override
	public void run() {
		before = after;
		System.out.println(EnergyDiff.between(before, after).dump());
		after = monitor.getSample();
	}
}

public class Monitor
{
	private int samplingRate;
	private final SyncEnergyMonitor monitor;
	private TimerTask dbSubmitTask;

	public Monitor() {
		monitor = new SyncEnergyMonitor();
		samplingRate = 15000; // default every 15 seconds
	}

	public void init() {
		monitor.init();
	}

	public void dealloc() {
		monitor.dealloc();
	}

	private void writeToDB(EnergyDiff sample) {

	}

	private static void waitTill15() { // synchronize operations with every 15th second
		while (Instant.now().getEpochSecond() % 15 != 0);
		System.out.println(Instant.now());
	}

	public void startMonitoring(int ms) {
//		// EnergyStats before, after = monitor.getSample();
//		dbSubmitTask = new TimerTask() {
//			EnergyStats before, after = monitor.getSample();
//	
//			public void run() {
//				before = after;
//				System.out.println(EnergyDiff.between(before, after).dump());
//				after = monitor.getSample();
//			}
//		};

		//DbSubmit dbSumbitTask = new DbSubmit();

		System.out.println(monitor.getSample().dump());

		Timer timer = new Timer("Timer");

		long delay = 1000L;
		long period = 1000L * 60L * 60L * 24L;
		timer.scheduleAtFixedRate(new DbSubmit(), delay, period);
	}

	public void abortMonitoring() {

	}

	public static void main(String[] args) throws InterruptedException
	{
		//for(int x = 0; x < 2; x++) { waitTill15(); Thread.sleep(1000); }
		Monitor m = new Monitor();
		m.init();
		m.startMonitoring(10000);
		m.dealloc();
	}
}