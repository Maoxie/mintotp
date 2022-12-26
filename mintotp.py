#!/usr/bin/python3
"""
Usage:

1. Set your token:
```python
echo your_token_here | python3 -m base64 -e > .secret
```

2. Run this script. Then the MF2 token will be set to the clipboard
```python
python mintotp.py
```

3. Now just paste the digits!
"""
import base64
import hmac
import os
import struct
import sys
import time


def hotp(key, counter, digits=6, digest='sha1') -> str:
    # key = base64.b32decode(key.upper() + '=' * ((8 - len(key)) % 8))
    key = base64.b64decode(key.upper() + '=' * ((8 - len(key)) % 8))
    counter = struct.pack('>Q', counter)
    mac = hmac.new(key, counter, digest).digest()
    offset = mac[-1] & 0x0f
    binary = struct.unpack('>L', mac[offset:offset+4])[0] & 0x7fffffff
    return str(binary)[-digits:].rjust(digits, '0')


def totp(key, time_step=30, digits=6, digest='sha1', verbose=True) -> str:
    epoch = int(time.time() % time_step)
    if time_step - epoch <= 3:
        wait(time_step - epoch, verbose)
    return hotp(key, int(time.time() / time_step), digits, digest)


def write_clipboard(text: str):
    platform = check_os()
    is_pastable = False
    if platform == "Windows":
        os.system("cmd /c echo " + text + "| clip")
        is_pastable = True
    elif platform in ("Linux", "MacOS"):
        os.system('echo "' + text + '" | pbcopy')
        is_pastable = True
    return is_pastable


def wait(seconds: int, verbose=True):
    platform = check_os()
    if platform == "Windows":
        if verbose:
            os.system(
                'cmd /c echo "Hold on, and wait {} seconds!"'.format(seconds)
                + ' && timeout /T {} /NOBREAK'.format(seconds)
            )
        else:
            os.system(
                'cmd /c timeout /T {} /NOBREAK'.format(seconds)
            )
    elif platform in ("Linux", "MacOS"):
        if verbose:
            os.system(
                'echo "Hold on, and wait {} seconds!"'.format(seconds)
                + ' && sleep {}'.format(seconds)
            )
        else:
            os.system(
                'sleep {}'.format(seconds)
            )
    else:
        if verbose:
            print("Hold on, and wait {} seconds!".format(seconds))
        time.sleep(3)


def check_os():
    platform = sys.platform.lower()
    if platform.startswith("linux"):
        return "Linux"
    elif platform.startswith("darwin"):
        return "MacOS"
    elif platform.startswith("win"):
        return "Windows"
    else:
        return "Unknown"



def main(verbose=True) -> str:
    with open(".secret", "r") as f:
        key = f.readline()
    token = totp(key, verbose=verbose)
    if verbose:
        print("The token is: {}".format(token))

    write_clipboard(token)
    if verbose:
        print("Now you can paste it anywhere.")
    return token


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    token = main(args.verbose)
    if not args.verbose:
        print(token + "\n")
