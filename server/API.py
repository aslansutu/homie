#! /bin/python3

from ping3 import ping
import sys


def is_online(host: str):
    """Checks if device is online

    Args:
        host: IP address or DNS name of device

    Returns:
        True if online, False if offline
    """
    return bool(ping(host))

def shutdown(host: str):
    if sys.platform.startswith('linux'):
        print('shutdown')
        
        
if __name__ == "__main__":
        print(is_online('10.143.0.1'))