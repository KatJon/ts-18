#!/bin/bash
./zad1.py -e infile.dat framed.dat
./zad1.py -d framed.dat copy.dat

diff infile.dat copy.dat
