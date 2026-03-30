# Copyright 2026 Mosoro Inc.
# SPDX-License-Identifier: Apache-2.0

"""Mosoro REST API Client."""

import logging
from typing import Any, Dict, List, Optional

import httpx

logger = logging.getLogger("mosoro.sdk.client")


class MosoroClient:
    """Synchronous client for the Mosoro REST API.

    Args:
        base_url: Base URL of the Mosoro API (e.g., "http://localhost:8000")
        token: Optional JWT token for authentication
        timeout: Request timeout in seconds
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        token: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self._client = httpx.Client(
            base_url=self.base_url,
            headers=headers,
            timeout=timeout,
        )

    def health(self) -> Dict[str, Any]:
        """Check API health."""
        response = self._client.get("/health")
        response.raise_for_status()
        return response.json()

    def list_robots(self) -> List[Dict[str, Any]]:
        """List all robots with current status."""
        response = self._client.get("/robots")
        response.raise_for_status()
        return response.json()

    def get_robot(self, robot_id: str) -> Dict[str, Any]:
        """Get a specific robot's status."""
        response = self._client.get(f"/robots/{robot_id}")
        response.raise_for_status()
        return response.json()

    def assign_task(
        self,
        robot_id: str,
        task_type: str,
        destination: Optional[Dict[str, float]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Assign a task to a robot."""
        payload = {
            "robot_id": robot_id,
            "task_type": task_type,
            **kwargs,
        }
        if destination:
            payload["destination"] = destination
        response = self._client.post("/tasks", json=payload)
        response.raise_for_status()
        return response.json()

    def get_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent fleet events."""
        response = self._client.get("/events", params={"limit": limit})
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
