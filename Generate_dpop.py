import time
import json
import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import string
import secrets
def generate_random_string(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_dpop(url, method, ephemeral_key_pair):
    now = int(time.time())
    
    payload = {
        "htu": url,
        "htm": method,
        "jti": generate_random_string(40),
        "iat": now,
        "exp": now + 120,
    }

        
    private_key_pem = ephemeral_key_pair["privateKey"]
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    x_b64 = jwt.utils.base64url_encode(public_key.public_numbers().x.to_bytes(32, byteorder='big'))
    y_b64 = jwt.utils.base64url_encode(public_key.public_numbers().y.to_bytes(32, byteorder='big'))
    jwk = {
        "kty": "EC",
        "kid": "kid",
        "crv": "P-256",
        "x": x_b64.decode('utf-8'),
        "y": y_b64.decode('utf-8'),
        "use": "sig",
        "alg": "ES256",
    }

    try:
        # Use PyJWT for encoding
        dpop = jwt.encode(
            payload,
            private_key,
            algorithm="ES256",
            headers={"typ": "dpop+jwt", "jwk": jwk},
        )
    except Exception as e:
        print(f"Error encoding JWT: {e}")
        return None
    
    return dpop

 
# Replace the following strings with your actual PEM-encoded key strings
private_key_pem = """
-----BEGIN EC PRIVATE KEY-----

-----END EC PRIVATE KEY-----
"""

public_key_pem = """
-----BEGIN PUBLIC KEY-----

-----END PUBLIC KEY-----
"""

ephemeral_key_pair = {
    "privateKey": private_key_pem,
    "publicKey": public_key_pem,
}

url = "https://example.com"
method = "POST"

dpop_token = generate_dpop(url, method, ephemeral_key_pair)

if dpop_token:
    print("Generated DPoP Token:")
    print(dpop_token)
else:
    print("Error generating DPoP Token.")
    
