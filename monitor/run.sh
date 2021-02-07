#!/bin/bash

if [ -z $1 ]; then
	name=Monitor
else
	name=$1
fi

sudo java -cp target/energyOracle-1.0-SNAPSHOT.jar:.:src/lib/jRAPL.jar energyOracle.$name
