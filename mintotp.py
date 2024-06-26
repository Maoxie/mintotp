#!/usr/bin/env python3
# -*- coding=utf-8 -*-
"""
Author: YANG Zhitao

Usage:

1. Set your token:

```bash
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
from pathlib import Path


def hotp(key: str, counter, digits=6, digest="sha1") -> str:
    key = key.upper() + "=" * ((8 - len(key)) % 8)
    key = base64.b32decode(key.encode("utf8"))
    counter = struct.pack(">Q", counter)
    mac = hmac.new(key, counter, digest).digest()
    offset = mac[-1] & 0x0F
    binary = struct.unpack(">L", mac[offset : offset + 4])[0] & 0x7FFFFFFF
    return str(binary)[-digits:].rjust(digits, "0")


def totp(key: str, time_step=30, digits=6, digest="sha1", verbose=True) -> str:
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
                + " && timeout /T {} /NOBREAK".format(seconds)
            )
        else:
            os.system("cmd /c timeout /T {} /NOBREAK".format(seconds))
    elif platform in ("Linux", "MacOS"):
        if verbose:
            os.system(
                'echo "Hold on, and wait {} seconds!"'.format(seconds)
                + " && sleep {}".format(seconds)
            )
        else:
            os.system("sleep {}".format(seconds))
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
    secret_file = Path(__file__).with_name(".secret")
    if not secret_file.exists():
        print("No token found.")
        print("Please following `README.md` to set your token first.")
        print()
        input("Press Any Key to exit...")
        sys.exit(1)

    with Path(__file__).with_name(".secret").open("r") as f:
        line = f.readline().strip()
        try:
            key = base64.decodebytes(line.encode("utf-8")).decode("utf8").strip()
        except Exception as e:
            print("The token is invalid.")
            print("Please following `README.md` to set your token again.")
            print()
            input("Press Any Key to exit...")
            sys.exit(1)

    token = totp(key, verbose=verbose)
    if verbose:
        print("The token is: {}".format(token))
    else:
        print(token)

    write_clipboard(token)
    if verbose:
        print("Now you can paste it anywhere.")
    return token


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    try:
        token = main(args.verbose)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print()
        input("Press Any Key to exit...")
        sys.exit(1)
