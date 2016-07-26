# IPv6DNSExfil

This script will create AAAA records that can be used as a C&C channel.
The output of the file2ipv6.sh script is intended to be piped to nsupdate,
which will then take care of sending the updates to the appropriate 
authoritative DNS server.

You will need to configure the correct DNS server in the script, as well as 
the zone you want to use for the C&C channel.

To run the script:

```bash
./file2ipv6 sample.txt | nsupdate -k dns.key  
```

sample.txt is any file that you would like to encode. Typically a simple 
text file with a shell command to be executed.
dns.key is the update key for your DNS server. This is optional, and if you need it or not will depend on your name server configuration.

More details: <https://isc.sans.edu/diary.html?storyid=21301>
