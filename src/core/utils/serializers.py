"""Encoders and decoders for JSON serialization."""
import json
from datetime import datetime
from typing import Any

from bson import ObjectId


class Encoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, bytes):
            return o.decode("utf-8")
        return json.JSONEncoder.default(self, o)
