# energyOracle
HackBU 2021

This project is used to predict computer energy consumption. It uses an open source Java library for energy reading to implement a scheduled monitor to run as a backgroundprogram for an extended period of time. It then uses the historical energy data to train a time series forecast and predict future energy consumption.


This type of tool is useful in the area of energy aware programming. As energy consumption increases, so does the demand for energy efficient systems. Energy
aware programming is an ongoing field of research to find ways to give programmers more access to their computers' energy usage, so they can easily write
energy efficient code and create programs to keep energy levels in check.

## RAPL and jRAPL
RAPL stands for Runtime Average Power Limiting. It's an interface to a set of Model Specfic Registers which report real-time energy activity across
different power comonents, such as DRAM, GPU, Core, and Package. We take advantage of this utility. There are plenty of other utilities, such as reporting thermal and power data, or writing
to the registers and setting power / thermal / etc limits over windows of time, in order to meet the demands of whatever optimal energy behavior the programmer
decides.

jRAPL is a high-level Java implementation of RAPL readings. The registers were originally intended for chip-level power management, but jRAPL takes it to the application level. The low level gathering is done in C subroutines called in a Java program via the Java Native Interface.

JRAPL was originally authored by Kenan Liu, a Binghmaton Alumnus under the supervision of Yu David Liu. I (Alejandro) for the past few semesters have taken some basic jRAPL code and am adding features for more functionality and accessibility. I used the energy getting library in order to implement our background monitor: a Java program that periodically takes energy readings and stores them in a time series database.

My jRAPL repo: [here](https://github.com/aservet1/jRAPL)

An unaffiliated group of researchers, the Green Software Lab, made use of jRAPL as part of their tool that profiles energy-inefficient parts of different
programming lanugages, finding key points of what they call "energy leaks." For further reading on the tool and the alogirithms they used, see their research
paper: [here](https://scihubtw.tw/10.1016/j.jss.2019.110463)

## Time Series Forecasting
We use time series forecasts with python's `fbprophet` module. It interfaces well with our time series database, InfluxDB, making it easy to collect the
data and focus on creating an accurate model. Our team mate used this type of technology at a part time job where he forecasted demand for his company's
data backup services.

## Desktop GUI Frontend
We created a GUI desktop application to interface with our backend tools with Python's TKinter module. We were able to create a user friendly interface (with a cool on-the-fly digital art logo !!) to display historical and predicted data parsed by Pandas and rendered with Matplotlib. We were able to get live updates of the state of our database as the monitor program gives updates. Every four hours, it predicts a new model based on the now updated historical data. Currently, we can only predict an hour or two into the future with relative accuracy, altough we've seen that as our monitor runs for longer, collecting more data, the models we generated become more and more accurate. We're confident that upon having a consistent week's worth of data, we can reliably predict forecasts of several days
into the future.

The GUI also informs the user of what the tool does and is meant to do, also warning that some operations around MSR interfacing require root access,
links to our source code for the user to inspect, and gives them a chance to leave the application without dipping into sudo-territory if they wish not to
do so.

## Potential for Extension
There were a lot of ideas that we had that we can do with this, which (much to our dismay) could not be done in a 24 hour time frame.

This type of program can be very useful to a server farm, one of the most notorious culprits of energy overconsumption. With accurate predictions (and the massive amounts of energy data they'd be able to generate, store and process) these forecasts could prove to be reliable ways to schedule future activities and energy controls. We were
thinking of having this system run on several computers and pool its data in a central server. The data coming from different machines would have made a
possibly more  interesting and in depth analysis of the data.

Another idea we had was to schedule energy limiting methods such as RAPL powercapping or Dynamic Volatage and Frequency Scaling (DVFS). As mentioned before, RAPL
provides powercap functionality by writing values to the MSRs. The programmer can target key predicted areas of energy usage and schedule the proper powercaps
over the correct time window, all facilitated by MSR writing. Writing to the MSRs was already implemented in the C library, and porting it to Java would not be a
difficult task. These pages of Intel's hardware manuals describe MSR interfacing: [here]( https://github.com/aservet1/jRAPL/blob/master/Docs/ReferenceDocuments/IntelManual_MSR-Pages.pdf). Dynamic Voltage and Frequency Scaling can also be implemented in response to predicted energy activity. Linux systems provide an easy DVFS interface by writing to system files that determine frequencies for cores and the frequency - governing procedure. See for more info: [here](https://github.com/aservet1/jRAPL/blob/master/Docs/ReferenceDocuments/CPUfreq_Governors.txt). There is an inverse relationship between frequency and voltage, so
making some calculations based off of the forecast is just a matter of applying the frequency \<=\> voltage formula, increasing or decreaing the frequency to get
optimal energy outputs. Power Capping and DVFS are used by my PhD research colleagues to implement an energy efficient java virtual machine. See more: [here](https://github.com/kliu20/EnergyAwareJVM)

There's a lot of research that can be done with this type of tool as energy consumption becomes a hotter topic, both with its financial and (more imporantly)
environmental impacts. Open source energy aware programs are currently few and far between, and there is a lot of research to be done in this area.
