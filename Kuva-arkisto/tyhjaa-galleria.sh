#!/bin/sh --

if [ "X$1" = "X" ] ; then
    echo Käyttö: $0 vuosi
    exit 1
fi

rm -f $1/*
rm -f $1/thumbs/*

cat gallery-head.html gallery-tail.html | sed s/XXXX/$1/g > $1/index.html
