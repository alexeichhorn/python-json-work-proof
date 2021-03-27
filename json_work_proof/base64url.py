import base64

def base64url_encode(value): # returns bytes
    if isinstance(value, str): value = value.encode('utf-8')
    encoded = base64.b64encode(value)
    stripped = encoded.split(b"=")[0]
    filtered = stripped.replace(b"+", b"-").replace(b"/", b"_")
    return filtered


def base64url_decode(arg):
    filtered = arg.replace("-", "+").replace("_", "/")
    padded = filtered + "=" * ((len(filtered) * -1) % 4)
    return base64.b64decode(padded)