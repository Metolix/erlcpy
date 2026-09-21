import time

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from erlcpy.webhooks import verify_signature


def test_valid_signature() -> None:
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key().public_bytes_raw()
    timestamp = str(int(time.time()))
    body = b'{"event":"test"}'
    signature = private_key.sign(timestamp.encode() + body).hex()

    assert verify_signature(
        timestamp,
        signature,
        body,
        public_key=public_key.hex(),
    )


def test_invalid_signature() -> None:
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key().public_bytes_raw()
    timestamp = str(int(time.time()))
    body = b'{"event":"test"}'
    signature = private_key.sign(timestamp.encode() + body).hex()

    assert not verify_signature(
        timestamp,
        signature,
        b'{"event":"changed"}',
        public_key=public_key.hex(),
    )
