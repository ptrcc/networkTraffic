from socket import socket, AF_INET, SOCK_RAW, IPPROTO_TCP, inet_ntoa, gethostbyname
from struct import unpack

from networkTraffic import Packet
from networkTraffic.ip_location_service import IPLocationService

_socket = socket(AF_INET, SOCK_RAW, IPPROTO_TCP)
_ip_location_srv = IPLocationService()

# ignore location service
_ignored_ip = gethostbyname('ipapi.co')

while True:
    packet = _socket.recvfrom(65565)[0]
    ip_header_packed = packet[0:20]
    ip_header = unpack('!BBHHHBBH4s4s', ip_header_packed)
    src_addr = inet_ntoa(ip_header[8])

    if src_addr != _ignored_ip:
        dest_addr = inet_ntoa(ip_header[9])
        version_ihl = ip_header[0]
        ttl = ip_header[5]
        ip_header_len = version_ihl & 0xF * 4

        packed_tcp_header = packet[ip_header_len:ip_header_len + 20]
        tcp_header = unpack('!HHLLBBHHH', packed_tcp_header)
        source_port = tcp_header[0]
        dest_port = tcp_header[1]
        tcp_header_len = tcp_header[4] >> 4

        packet = Packet(
            src_port=source_port,
            dest_port=dest_port,
            src_addr=src_addr,
            dest_addr=dest_addr,
            ip_header_len=ip_header_len,
            tcp_header_len=tcp_header_len,
            ttl=ttl,
            src_addr_location=_ip_location_srv.get_ip_location(src_addr)
        )

        print(packet)
