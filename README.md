# mintotp

Usage:

## 1. Encode your token and set it as the `KEY` below

```bash
echo your_token_here | python3 -m base64 -e > .secret
```

## 2. Run this script. Then the MF2 token will be set to the clipboard

```python
python mintotp.py
```

## 3. Now just paste the token!
