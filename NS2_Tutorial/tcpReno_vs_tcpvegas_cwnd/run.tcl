#!bin/tcl
for {set index 0} { $index < 3 } { incr index } {
    exec ns reno_vs_vegas.tcl $index
}
