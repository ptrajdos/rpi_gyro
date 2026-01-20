import socket
import random


def get_unused_port(min_port=1025, max_port=65535):
    while True:
        port = random.randint(min_port, max_port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Try to bind the socket to the port
            try:
                s.bind(("", port))
                return port  # If successful, the port is unused
            except OSError:
                continue  # If binding fails, try another port


def get_unused_ports(count=5, min_port=1025, max_port=65535):
    ports = set()
    while len(ports) < count:
        port = random.randint(min_port, max_port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))  # Attempt to bind to the port
                ports.add(port)  # If successful, add it to the set
            except OSError:
                continue  # If binding fails, try another port
    return ports

