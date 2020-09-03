# main.tcl
# topology:
#  n1___               __n5
#       |___n3____n4__|
#  n2___|             |__n6

#  n1 and n2 are tcp senders
#  n5 and n6 are tcp sinks
#  n3 and n4 are routers with limited queue
#  n1 and n2 are running FTP over TCP connection
#  flow 0 :: src=n1  dst=n5
#  flow 1 :: src=n2  dst=n6

# !!! run script like: "ns main.tcl  agent  n23_d  n46_d  ftr  fnm"
#  * agent: choose from {Agent/TCP(aka.Tahoe), Agent/TCP/Vegas, Agent/TCP/Newreno}
#  * n23_d: delay of link between n2 and n3
#  * n46_d: delay of link between n4 and n6
#  * ftr  : trace file name(eg. "random.tr")
#  * fnm  : nam file name(eg. "random.nam")


# link speeds
set n13_speed 100Mb
set n23_speed 100Mb
set n34_speed 100Kb
set n45_speed 100Mb
set n46_speed 100Mb

# link delays
set n13_daley 5ms
set n23_daley [lindex $argv 1]
set n34_daley 1ms
set n45_daley 5ms
set n46_daley [lindex $argv 2]

# tcp agent
set agent    [lindex $argv 0]

# trace file and nam file
set ftr_name [lindex $argv 3]
set fnm_name [lindex $argv 4]

# Router Queue Size
set q_size 10

# simulation intervals
set sim_start 0.0
set sim_finish [lindex $argv 5]

# -------------------------------------------------------------------------------------------------
	
#Create a simulator object
set ns [new Simulator]

#Open the nam file basic1.nam and the variable-trace file basic1.tr
set namfile   [open $fnm_name w]
set tracefile [open $ftr_name w]
$ns namtrace-all $namfile
$ns trace-all    $tracefile

#Define a 'finish' procedure
proc finish {} {
	global ns namfile tracefile
	$ns flush-trace
	close $namfile
	close $tracefile
	# To see the graphical simulation at the end
	# exec nam test &
	exit 0
}

#Create the network nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

#Create a duplex link between the nodes(total of 5 links needed)
$ns duplex-link $n1 $n3 $n13_speed $n13_daley DropTail
$ns duplex-link $n2 $n3 $n23_speed $n23_daley DropTail
$ns duplex-link $n3 $n4 $n34_speed $n34_daley DropTail
$ns duplex-link $n4 $n5 $n45_speed $n45_daley DropTail
$ns duplex-link $n4 $n6 $n46_speed $n46_daley DropTail

# The queue size in routers are {q_size}
# $ns queue-limit $n1 $n3 $q_size
# $ns queue-limit $n2 $n3 $q_size
$ns queue-limit $n3 $n4 $q_size
$ns queue-limit $n4 $n3 $q_size
# $ns queue-limit $n4 $n5 $q_size
# $ns queue-limit $n4 $n6 $q_size

#Monitor the queue
$ns duplex-link-op $n3 $n4 queuePos 0.5


# some hints for nam
# color packets of flow 0 red
$ns color 0 Red
$ns color 1 Blue
$ns duplex-link-op $n1 $n3 orient right-down
$ns duplex-link-op $n2 $n3 orient right-up
$ns duplex-link-op $n3 $n4 orient right
$ns duplex-link-op $n4 $n5 orient right-up
$ns duplex-link-op $n4 $n6 orient right-down


# Create a TCP agents
set tcp0 [new $agent]
$tcp0 set class_ 0
$ns attach-agent $n1 $tcp0

set tcp1 [new $agent]
$tcp1 set class_ 1
$ns attach-agent $n2 $tcp1

# trace some vars
$tcp0 attach $tracefile
$tcp0 tracevar cwnd_
$tcp0 tracevar ssthresh_
$tcp0 tracevar ack_
$tcp0 tracevar maxseq_
$tcp0 tracevar nrexmitpack_
$tcp0 tracevar rtt_

$tcp1 attach $tracefile
$tcp1 tracevar cwnd_
$tcp1 tracevar ssthresh_
$tcp1 tracevar ack_
$tcp1 tracevar maxseq_
$tcp1 tracevar nrexmitpack_
$tcp1 tracevar rtt_


#Create a TCP receive agent (a traffic sink)
set end0 [new Agent/TCPSink]
$ns attach-agent $n5 $end0

set end1 [new Agent/TCPSink]
$ns attach-agent $n6 $end1

#Connect the traffic source with the traffic sink
$ns connect $tcp0 $end0
$ns connect $tcp1 $end1

# setup applications to run over tcp agents
set ftp0 [new Application/FTP]
$ftp0 attach-agent $tcp0

set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1

# # RTT Calculation Using Ping ------------------------------------------------

# set p0 [new Agent/Ping]
# $ns attach-agent $n1 $p0
# set p1 [new Agent/Ping]
# $ns attach-agent $n5 $p1

# #Connect the two agents
# $ns connect $p0 $p1

# # Method call from ping.cc file
# Agent/Ping instproc recv {from rtt} {
# $self instvar node_
# puts "node [$node_ id] received ping answer from \
# $from with round-trip-time $rtt ms."
# }

# $ns at 0.0 "$p0 send"
# $ns at 0.0 "$p1 send"

# # ---------------------------------------------------------------------------

#Schedule the connection data flows
$ns at $sim_start "$ftp0 start"
$ns at $sim_start "$ftp1 start"
$ns at $sim_finish "finish"

#Run the simulation
$ns run