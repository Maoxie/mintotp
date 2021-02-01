# mintotp

Usage:

## 1. Encode your token and set it as the `KEY` below

```python
import base64
base64.encodebytes('your_token'.encode('utf8'))
```

## 2. Run this script. Then the MF2 token will be set to the clipboard

```python
python mintotp.py
```

## 3. Now just paste the token!
