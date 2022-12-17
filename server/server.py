#! /bin/python3

from fastapi import FastAPI
import uvicorn

from fastapi.responses import HTMLResponse

import subprocess
import nmap
import socket
from wakeonlan import send_magic_packet

app = FastAPI()

DEVICES = {"192.168.1.111": {'username': 'Atakan', 'password': 'Ataturkum4!', 'mac_address': '74.D4.35.5E.B2.BC', 'os': 'Windows'}}

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Hanifoş</title>
        </head>
        <body>
            <h1>Aşkım, hayatım, canım, biricik sevgilim, Hanife seni çok seviyorum!</h1>
        </body>
    </html>
    """
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")