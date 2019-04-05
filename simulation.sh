#!/bin/bash

num_to_run=${1}
shift 1
boot_ip=${1}
shift 1
boot_port=${1}
shift 1

echo "Running simulation with bootstrap node ${boot_ip}:${boot_port}..."
echo "Launching ${num_to_run} active nodes"

for i in $(seq 1 ${num_to_run})
do
    port=`expr ${boot_port} + ${i}`
    python3 kad_sim.py ${boot_ip} ${port} ${boot_ip} ${boot_port} &
    sleep 1
done

