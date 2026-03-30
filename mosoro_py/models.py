# Copyright 2026 Mosoro Inc.
# SPDX-License-Identifier: Apache-2.0

"""Re-exported Pydantic models from mosoro-core.

If mosoro-core is installed, models are imported from there.
Otherwise, minimal standalone definitions are provided.
"""

try:
    from mosoro_core.models import (
        CurrentTask,
        ErrorDetail,
        MessageHeader,
        MosoroMessage,
        MosoroPayload,
        Position,
    )
except ImportError:
    # Standalone minimal definitions for SDK-only usage
    from pydantic import BaseModel, Field
    from typing import Any, Dict, List, Optional
    from datetime import datetime

    class Position(BaseModel):
        x: float
        y: float
        z: Optional[float] = None
        theta: Optional[float] = None
        map_id: Optional[str] = None

    class CurrentTask(BaseModel):
        task_id: str
        task_type: str
        progress: Optional[float] = 0.0

    class ErrorDetail(BaseModel):
        code: str
        message: str

    class MessageHeader(BaseModel):
        message_id: str = ""
        version: str = "1.0"
        correlation_id: Optional[str] = None

    class MosoroPayload(BaseModel):
        position: Optional[Position] = None
        battery: Optional[float] = None
        status: Optional[str] = None
        current_task: Optional[CurrentTask] = None
        health: Optional[str] = None
        errors: Optional[List[ErrorDetail]] = None
        vendor_specific: Optional[Dict[str, Any]] = None

    class MosoroMessage(BaseModel):
        header: MessageHeader = Field(default_factory=MessageHeader)
        robot_id: str
        vendor: str
        timestamp: datetime = Field(default_factory=datetime.utcnow)
        type: str
        payload: MosoroPayload = Field(default_factory=MosoroPayload)


__all__ = [
    "MosoroMessage",
    "MosoroPayload",
    "Position",
    "MessageHeader",
    "CurrentTask",
    "ErrorDetail",
]
