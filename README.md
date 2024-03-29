# mintotp

Get your 2FA token, run the script and paste it anywhere!

## Dependencies

Only python>=3.6 is required.

## Usage

### 1. Setup your token

Create a file named `.secret` and write your encoded token in it.

```python
import base64
key = base64.encodebytes('your_token_here'.encode('utf8'))
with open('.secret', 'w') as f:
    f.write(key.decode('utf8'))
```

Copy the above outputs to `.secret`

--- OR ---

Just do this in one line!

```bash
echo your_token_here | python3 -m base64 -e > .secret
```

### 2. Run this script when you need

Then the 2FA token will be write to the clipboard

```python
python mintotp.py
# or:
# python mintotp.py --verbose
```

#### Tips for windows users

It's recommended to use [PowerToys Run](https://learn.microsoft.com/en-us/windows/powertoys/run) of [PowerToys](https://learn.microsoft.com/en-us/windows/powertoys/) or any other starters to quickly run the script.

There is a batch file for you: `.\mintotp.bat`. Create a shortcut for it in the start menu or on the desktop, then starters can find it.

### 3. Now you can paste

## FAQ

### Q1: I run the script but nothing happens

A1:

Please make sure you have `python` command available in your terminal.

If you are using `conda`, since `cmd` will not activate the environment before running batch file,
you may need to install another python in your system.

You can check your python by running in your cmd:

```cmd
conda deactivate
python --version
```

Please make sure the version is greater than `3.6`
