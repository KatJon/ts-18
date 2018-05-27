#!/bin/bash
java Z2Receiver 6002 6003 > rec_fwd.log & 
REC=$!
java Z2Forwarder 6001 6002 &
FWD1=$!
java Z2Forwarder 6003 6000 &
FWD2=$!
java Z2Sender 6000 6001 < plik.txt
kill ${FWD2}
kill ${FWD1}
kill ${REC}
