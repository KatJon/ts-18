#!/bin/bash
for i in {1..10}; do
    ./gen.py                            # generate data.in
    ./zad1.py -e data.in framed.dat     # encode
    ./zad1.py -d framed.dat data.out    # decode
    diff data.in data.out               # check if equal
done

rm data.in framed.dat data.out