from erlcpy.webhooks import verify_signature


def test_invalid_signature_returns_false() -> None:
    assert verify_signature(
        "123",
        "00" * 64,
        b"{}",
        public_key="00" * 32,
    ) is False
