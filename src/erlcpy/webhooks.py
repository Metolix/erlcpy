from __future__ import annotations

import base64
import binascii


class WebhookVerificationError(ValueError):
    pass


def _load_public_key(value: str):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    from cryptography.hazmat.primitives import serialization

    candidates: list[bytes] = []
    try:
        candidates.append(bytes.fromhex(value))
    except ValueError:
        pass
    try:
        candidates.append(base64.b64decode(value, validate=True))
    except (ValueError, binascii.Error):
        pass

    for data in candidates:
        if len(data) == 32:
            return Ed25519PublicKey.from_public_bytes(data)
        try:
            return serialization.load_der_public_key(data)
        except ValueError:
            continue

    raise WebhookVerificationError("Invalid Ed25519 public key.")


def verify_signature(
    timestamp: str,
    signature: str,
    body: bytes,
    *,
    public_key: str,
) -> bool:
    try:
        from cryptography.exceptions import InvalidSignature
    except ImportError as exc:
        raise RuntimeError(
            'Install "erlcpy[webhooks]" to verify webhook signatures.'
        ) from exc

    try:
        signature_bytes = bytes.fromhex(signature)
    except (ValueError, binascii.Error) as exc:
        raise WebhookVerificationError("Invalid webhook signature.") from exc

    try:
        key = _load_public_key(public_key)
        key.verify(signature_bytes, timestamp.encode("utf-8") + body)
    except InvalidSignature:
        return False

    return True
