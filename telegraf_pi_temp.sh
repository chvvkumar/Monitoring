#!/bin/bash
prefix="temp="
suffix="'C"
gpu=$(/opt/vc/bin/vcgencmd measure_temp)
gpu_temp=${gpu#$prefix}
gpu_temp=${gpu_temp%$suffix}
echo -e "{\"cpu\":"$(</sys/class/thermal/thermal_zone0/temp)", \"gpu\":$gpu_temp}"
