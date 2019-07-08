#!/usr/bin/env bash
EXE="./$1"
SAMPLES=$2
TIME="0.0"
for (( c=1; c<=$SAMPLES; c++ )) do
	TIME=$(python -c "print($TIME + $( $EXE ))")
done
TIME=$(python -c "print($TIME / $SAMPLES)")
echo "$TIME"