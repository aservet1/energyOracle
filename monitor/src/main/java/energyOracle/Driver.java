package energyOracle;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

// executing a shell command because i spent over an hour trying to get maven to properly package
// dependencies into a jar and it didnt work so now i have to use a shell command that properly
// points the classpath where it needs to go. quick fix so i can get on with the rest of the thing

// credit to: https://stackoverflow.com/questions/3062305/executing-shell-commands-from-java

public class Driver {
    public static void main(String... args) {
        String base = "/home/alejandro/Documents/Projects/hackbu2021/energyOracle/monitor";
        String command = "sudo java -cp "+base+":"+base+"/jRAPL.jar:"+base+"/target/energyOracle-1.0-SNAPSHOT.jar energyOracle.Monitor";
        try {
            
            Process cmdProc = Runtime.getRuntime().exec(command);

            BufferedReader stdoutReader = new BufferedReader(
                    new InputStreamReader(cmdProc.getInputStream()));
            String line;
            while ((line = stdoutReader.readLine()) != null) {
                System.out.println(line); // printing stdout
            }

            BufferedReader stderrReader = new BufferedReader(
                    new InputStreamReader(cmdProc.getErrorStream()));
            while ((line = stderrReader.readLine()) != null) {
                System.out.println(line); // printing stderr
            }

            int retValue = cmdProc.exitValue();
        } catch (IOException ex) {
            System.out.println("<<IOException trying to run command: " + command);
        }
    }
    
}
