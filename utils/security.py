import ssl
def create_ssl_context(certfile='cert.pem', keyfile='key.pem'):
    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    return ctx
def sign_task(payload, private_key): return "signed"
def verify_task(payload, signature, public_key): return True