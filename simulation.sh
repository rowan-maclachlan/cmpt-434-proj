#!/bin/bash

# This is the simulation script.  The user should start up a node via kad.py
# first, and make note of the IP and port number used to create it.
# Then, the user should run this script by providing the number of nodes they
# want to create, the IP they used for their first node, and the port number
# that node is listening on, as such:
#
# python kad.py 0.0.0.0 2000
# ./simulation.py 10 0.0.0.0 2000
#
# This will launch 10 nodes that attempt to bootstrap off of 0.0.0.0:2000.
# They listen on the same IP address but increment the port number.  This means
# that the user must create their first node with a port value at the beginning
# of a range of contiguous free ports.
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

