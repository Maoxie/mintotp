#!/usr/bin/python3
"""
Usage:

1. Set the `KEY`
```python
import base64
base64.encodebytes('copy_the_token_here'.encode('utf8'))
```

2. Run this script. Then the MF2 token will be set to the clipboard
```python
python mintotp.py
```

3. Now just paste the token!
"""
import base64
import hmac
import os
import struct
import time


KEY = 'PUT_YOUR_BASE64_ENCODED_TOKEN_HERE'

def hotp(key, counter, digits=6, digest='sha1'):
    key = base64.b32decode(key.upper() + '=' * ((8 - len(key)) % 8))
    counter = struct.pack('>Q', counter)
    mac = hmac.new(key, counter, digest).digest()
    offset = mac[-1] & 0x0f
    binary = struct.unpack('>L', mac[offset:offset+4])[0] & 0x7fffffff
    return str(binary)[-digits:].rjust(digits, '0')

def totp(key, time_step=30, digits=6, digest='sha1'):
    epoch = int(time.time() % time_step)
    if time_step - epoch <= 3:
        wait(time_step - epoch)
    return hotp(key, int(time.time() / time_step), digits, digest)

def write_clipboard(text: str):
    os.system("cmd /c echo " + text + "| clip")

def wait(seconds: int):
    os.system(f'cmd /c echo "Hold on, and wait {seconds} seconds!"'
              u' && timeout /T 3 /NOBREAK')

def Main():
    key = base64.decodebytes(KEY.encode('utf8')).decode('utf8')
    token = totp(key)
    write_clipboard(token)
    return token


if __name__ == '__main__':
    Main()
