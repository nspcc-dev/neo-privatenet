#!/bin/bash
#
# This script starts four consensus and waits forever
#

# Create log fifos
[[ -p node1.log ]] || mkfifo node1.log
[[ -p node2.log ]] || mkfifo node2.log
[[ -p node3.log ]] || mkfifo node3.log
[[ -p node4.log ]] || mkfifo node4.log
[[ -p contract.log ]] || mkfifo contract.log

# Merge all node's screen logs to one output
( while read -r line; do echo "node1: $line"; done < node1.log ) &
( while read -r line; do echo "node2: $line"; done < node2.log ) &
( while read -r line; do echo "node3: $line"; done < node3.log ) &
( while read -r line; do echo "node4: $line"; done < node4.log ) &
( while read -r line; do echo "contract: $line"; done < contract.log ) &

# Start nodes 
screen -dmSL node1 -Logfile node1.log expect /opt/start_consensus_node.sh /opt/node1/neo-cli/ wallet1.json one
screen -dmSL node2 -Logfile node2.log expect /opt/start_consensus_node.sh /opt/node2/neo-cli/ wallet2.json two
screen -dmSL node3 -Logfile node3.log expect /opt/start_consensus_node.sh /opt/node3/neo-cli/ wallet3.json three
screen -dmSL node4 -Logfile node4.log expect /opt/start_consensus_node.sh /opt/node4/neo-cli/ wallet4.json four

# Remove that before we run
rm -rf /root/.neopython/Chains/privnet*

# Import SmartContract
screen -dmSL contract -Logfile contract.log python3 /scripts/import.py

# infinite loop (fast stop)
sleep infinity
