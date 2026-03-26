# Copyright 2026 Mosoro Inc.
# SPDX-License-Identifier: Apache-2.0

"""Mosoro MQTT Client Wrapper."""

import json
import logging
from typing import Any, Callable, Dict, Optional

from paho.mqtt import client as mqtt

logger = logging.getLogger("mosoro.sdk.mqtt")


class MosoroMQTT:
    """MQTT client wrapper for subscribing to Mosoro fleet events.
    
    Args:
        broker: MQTT broker hostname
        port: MQTT broker port
        client_id: Optional MQTT client ID
        tls_config: Optional TLS configuration dict
    """

    def __init__(
        self,
        broker: str = "localhost",
        port: int = 1883,
        client_id: Optional[str] = None,
        tls_config: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.broker = broker
        self.port = port
        self._handlers: Dict[str, list[Callable]] = {}
        self._client = mqtt.Client(
            client_id=client_id or "",
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        )
        self._client.on_message = self._on_message
        
        if tls_config:
            self._client.tls_set(**tls_config)

    def on_status(self, robot_id: str) -> Callable:
        """Decorator to register a handler for robot status updates."""
        topic = f"mosoro/v1/agents/{robot_id}/status"
        def decorator(func: Callable) -> Callable:
            if topic not in self._handlers:
                self._handlers[topic] = []
            self._handlers[topic].append(func)
            return func
        return decorator

    def on_event(self, robot_id: str) -> Callable:
        """Decorator to register a handler for robot events."""
        topic = f"mosoro/v1/agents/{robot_id}/events"
        def decorator(func: Callable) -> Callable:
            if topic not in self._handlers:
                self._handlers[topic] = []
            self._handlers[topic].append(func)
            return func
        return decorator

    def subscribe(self, topic: str, handler: Callable) -> None:
        """Subscribe to a topic with a handler function."""
        if topic not in self._handlers:
            self._handlers[topic] = []
        self._handlers[topic].append(handler)

    def connect(self) -> None:
        """Connect to the MQTT broker and start listening."""
        self._client.connect(self.broker, self.port)
        for topic in self._handlers:
            self._client.subscribe(topic)
            logger.info("Subscribed to %s", topic)
        self._client.loop_start()

    def disconnect(self) -> None:
        """Disconnect from the MQTT broker."""
        self._client.loop_stop()
        self._client.disconnect()

    def _on_message(self, client, userdata, msg) -> None:
        """Internal message handler that dispatches to registered handlers."""
        handlers = self._handlers.get(msg.topic, [])
        if not handlers:
            return
        try:
            payload = json.loads(msg.payload.decode())
        except (json.JSONDecodeError, UnicodeDecodeError):
            logger.warning("Failed to decode message on %s", msg.topic)
            return
        for handler in handlers:
            try:
                handler(payload)
            except Exception:
                logger.exception("Error in handler for %s", msg.topic)
