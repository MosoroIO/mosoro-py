"""Mosoro Python SDK — Client library for the Mosoro platform."""

from mosoro_py.client import MosoroClient
from mosoro_py.mqtt import MosoroMQTT
from mosoro_py.models import (
    CurrentTask,
    ErrorDetail,
    MessageHeader,
    MosoroMessage,
    MosoroPayload,
    Position,
)

__version__ = "0.1.0"
__all__ = [
    "MosoroClient",
    "MosoroMQTT",
    # Models (re-exported from mosoro-core or standalone)
    "MosoroMessage",
    "MosoroPayload",
    "Position",
    "MessageHeader",
    "CurrentTask",
    "ErrorDetail",
    "__version__",
]
