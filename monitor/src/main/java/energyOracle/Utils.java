package energyOracle;

import java.util.HashMap;
import java.time.Instant;

import jRAPL.EnergySample;
import jRAPL.EnergyStats;
import jRAPL.EnergyDiff;
import jRAPL.SyncEnergyMonitor;
import jRAPL.ArchSpec;

public class Utils {
    public static HashMap<String, HashMap<String,Double>> toHashMap(EnergySample energy) {
        HashMap<String, HashMap<String,Double>> M = new HashMap<String,HashMap<String,Double>>();
        for (int socket = 1; socket <= ArchSpec.NUM_SOCKETS; socket++) {
            HashMap<String,Double> m = new HashMap<String,Double>();
            m.put("DRAM", energy.atSocket(1).getDram());
            m.put("GPU", energy.atSocket(1).getGpu());
            m.put("CORE", energy.atSocket(1).getCore());
            m.put("PKG", energy.atSocket(1).getPackage());
            M.put("Socket"+socket,m);
        }
        // m.put("timestamp", Math.floor((double)Instant.now().getEpochSecond()),);
        return M;
    }
    public static void main(String... args) throws InterruptedException{
        SyncEnergyMonitor m = new SyncEnergyMonitor();
        m.init();
     
        EnergyStats before,after=m.getSample();
     
        for (int x = 0; x < 100 ; x++) {
            before = after;
            Thread.sleep(70);
            after = m.getSample();
            System.out.println(Utils.toHashMap(EnergyDiff.between(before,after)));
        }

        m.dealloc();
    }
}