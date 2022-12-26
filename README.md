# mintotp

Usage:

## 1. Encode your token and set it as the `KEY` below

```python
import base64
base64.encodebytes('your_token_here'.encode('utf8'))
```

Copy the above outputs to `.secret`

## 2. Run this script. Then the MF2 token will be set to the clipboard

```python
python mintotp.py
# or:
# python mintotp.py --verbose
```

## 3. Now just paste the token!
