# Copyright 2026 Mosoro Inc.
# SPDX-License-Identifier: Apache-2.0

"""Webhook signature validation helpers."""

import hashlib
import hmac
import logging
from typing import Optional

logger = logging.getLogger("mosoro.sdk.webhooks")


def validate_signature(
    payload: bytes,
    signature: str,
    secret: str,
    algorithm: str = "sha256",
) -> bool:
    """Validate a webhook payload signature.

    Args:
        payload: Raw request body bytes
        signature: Signature from the X-Mosoro-Signature header
        secret: Webhook secret key
        algorithm: Hash algorithm (default: sha256)

    Returns:
        True if signature is valid, False otherwise
    """
    expected = hmac.new(
        secret.encode(),
        payload,
        getattr(hashlib, algorithm),
    ).hexdigest()

    return hmac.compare_digest(expected, signature)


def parse_signature_header(header: str) -> Optional[str]:
    """Parse the X-Mosoro-Signature header value.

    Expected format: "sha256=<hex_digest>"

    Returns the hex digest portion, or None if invalid.
    """
    if not header or "=" not in header:
        return None
    parts = header.split("=", 1)
    if len(parts) != 2:
        return None
    return parts[1]
