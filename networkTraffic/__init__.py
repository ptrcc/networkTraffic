from dataclasses import dataclass


@dataclass
class Location:
    city: str
    country: str

    def __str__(self):
        return f"{self.city}:{self.country}"


@dataclass
class Packet:
    src_port: int
    dest_port: int
    src_addr: str
    dest_addr: str
    ttl: int
    ip_header_len: int
    tcp_header_len: int
    src_addr_location: Location

    def __str__(self):
        return f"""
source:      {self.src_addr}:{self.src_port}
destination: {self.dest_addr}:{self.dest_port}
location:    {self.src_addr_location}"""
