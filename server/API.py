#! /bin/python3

import subprocess

def shutdown(ip: str, username: str, password: str, os: str)
    cmd = 'net rpc -S ' + ip + ' -U ' + username + '%' + password ' shutdown -t 1 -f'
    subprocess.call(["net", "rpc", "-S", ])