from __future__ import annotations

import binascii


class WebhookVerificationError(ValueError):
    pass


def verify_signature(
    timestamp: str,
    signature: str,
    body: bytes,
    *,
    public_key: str,
) -> bool:
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives import serialization
    except ImportError as exc:
        raise RuntimeError(
            'Install "erlcpy[webhooks]" to verify webhook signatures.'
        ) from exc

    try:
        key_bytes = bytes.fromhex(public_key)
        signature_bytes = bytes.fromhex(signature)
        key = serialization.load_der_public_key(key_bytes)
    except (ValueError, binascii.Error, TypeError) as exc:
        raise WebhookVerificationError("Invalid webhook key or signature.") from exc

    try:
        key.verify(signature_bytes, timestamp.encode("utf-8") + body)
    except InvalidSignature:
        return False
    return True
