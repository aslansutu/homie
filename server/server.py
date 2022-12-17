#! /bin/python3

from fastapi import FastAPI

import subprocess
import nmap
import socket
from wakeonlan import send_magic_packet

app = FastAPI()

DEVICES = {"192.168.1.111": {'username': 'Atakan', 'password': 'Ataturkum4!', 'mac_address': '74.D4.35.5E.B2.BC', 'os': 'Windows'}}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/down/{ip}")
async def shutdown(ip: str):
    if ip not in DEVICES:
        print("IP address not configured")
        return 1

    username = DEVICES[ip]['username']
    password = DEVICES[ip]['password']

    if DEVICES[ip]['os'] == 'Windows':
        cmd = "net rpc shutdown -f -t 0 -C 'FastAPI_Remote_Shutdown' -U " + username + "%" + password + " -I " + ip
    if DEVICES[ip]['os'] == 'Linux':
        cmd = "ssh -t " + username + "@" + ip + "'sudo shutdown -h 0'" # TODO: Use Paramiko SSH client to shutdown

#    cmd = cmd.split(" ")

    result = subprocess.run(cmd.split(" "), capture_output=True, text=True)

    return {"output": result.stdout, "error": result.stderr}

@app.get("/up/{ip}")
async def boot(ip: str):
    result = send_magic_packet(DEVICES[ip]['mac_address'])
    return{"message": str(result)}

@app.get("/is-up/{ip}")
async def is_up(ip: str):
    scanner = nmap.PortScanner()
    host = socket.gethostbyname(ip)
    scanner.scan(host, '1', '-v')
    return {"IP Status:": scanner[host].state()}