# Copyright 2026 Mosoro Inc.
# SPDX-License-Identifier: Apache-2.0

"""Tests for the Mosoro Python SDK client."""

from mosoro_py.client import MosoroClient
from mosoro_py.webhooks import validate_signature, parse_signature_header


class TestMosoroClient:
    def test_client_creation(self):
        client = MosoroClient(base_url="http://localhost:8000")
        assert client.base_url == "http://localhost:8000"
        client.close()

    def test_client_strips_trailing_slash(self):
        client = MosoroClient(base_url="http://localhost:8000/")
        assert client.base_url == "http://localhost:8000"
        client.close()

    def test_client_context_manager(self):
        with MosoroClient() as client:
            assert client is not None


class TestWebhookValidation:
    def test_valid_signature(self):
        payload = b'{"event": "status_update"}'
        secret = "test-secret"
        import hashlib
        import hmac

        sig = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
        assert validate_signature(payload, sig, secret) is True

    def test_invalid_signature(self):
        assert validate_signature(b"payload", "invalid", "secret") is False

    def test_parse_signature_header(self):
        assert parse_signature_header("sha256=abc123") == "abc123"

    def test_parse_empty_header(self):
        assert parse_signature_header("") is None
        assert parse_signature_header(None) is None
