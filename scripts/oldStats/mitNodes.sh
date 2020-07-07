#!/bin/bash

total_nodes=`condor_status -pool t3serv007.mit.edu:11000?sock=collector -af Activity| wc -l`
busy_nodes=`condor_status -pool t3serv007.mit.edu:11000?sock=collector -af Activity| grep Busy| wc -l`
echo $total_nodes       $busy_nodes     $((total_nodes-busy_nodes))