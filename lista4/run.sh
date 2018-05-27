#!/bin/bash
java Z2Receiver 6001 6000 > rec.log&
REC=$!
java Z2Sender 6000 6001 < plik.txt
kill ${REC}