package sample;

import jRAPL.*;
import java.time.Instant;

public class Sample {
    public static void main(String... args) throws InterruptedException {
        System.out.println("socket,"+ArchSpec.ENERGY_STATS_STRING_FORMAT.split("@")[0]+",timestamp");
        SyncEnergyMonitor m = new SyncEnergyMonitor();
        m.init();
        EnergyStats before, after = m.getSample();
        EnergyDiff d;
        System.out.println("Started at: " + Instant.now());
        for(;;) {
            before = after;
            Thread.sleep(15000);
            after = m.getSample();
            d = EnergyDiff.between(before, after);
            System.out.println(d.dump()+","+
                Math.floor(Instant.now().getEpochSecond()/15)*15);
        }
        //m.dealloc();
    }
}
