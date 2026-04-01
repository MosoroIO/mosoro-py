# Mosoro Python SDK

[![CI](https://github.com/mosoroio/mosoro-py/actions/workflows/ci.yml/badge.svg)](https://github.com/mosoroio/mosoro-py/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/mosoro-py)](https://pypi.org/project/mosoro-py/)
[![Python](https://img.shields.io/pypi/pyversions/mosoro-py)](https://pypi.org/project/mosoro-py/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Official Python client library for [Mosoro](https://github.com/mosoroio/mosoro-core) — the open-source communication bridge for multi-vendor robot fleets.

## Installation

```bash
pip install mosoro-py
```

## Quick Start

```python
from mosoro_py import MosoroClient

client = MosoroClient(base_url="http://localhost:8000")

# List all robots
robots = client.list_robots()

# Get a specific robot
robot = client.get_robot("robot-locus-001")

# Assign a task
client.assign_task("robot-locus-001", task_type="pick", destination={"x": 10, "y": 20})

# Get recent events
events = client.get_events(limit=50)
```

## MQTT Streaming

```python
from mosoro_py import MosoroMQTT

mqtt = MosoroMQTT(broker="localhost", port=1883)

@mqtt.on_status("robot-locus-001")
def handle_status(message):
    print(f"Robot status: {message.payload.status}")

mqtt.connect()
```

## API Reference

See [Mosoro Documentation](https://docs.mosoro.io) for the full API reference.
