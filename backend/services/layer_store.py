import uuid
import time
from threading import Lock
from typing import Optional, Dict, Any

# Module-level state (shared across all requests)
_store: Dict[str, Dict[str, Any]] = {}
_lock = Lock()
TTL_SECONDS = 1800  # 30 minutes

def create_layer(sql_query: str, layer_name: str = None) -> str:
    layer_id = str(uuid.uuid4())
    
    with _lock:
        _store[layer_id] = {
            "sql": sql_query,
            "name": layer_name or f"layer_{layer_id[:8]}",
            "created": time.time()
        }
    print(f"[LayerStore] Created layer: {layer_id}: {layer_name}")
    return layer_id

def get_layer(layer_id: str) -> Optional[Dict[str, Any]]:
    with _lock:
        entry = _store.get(layer_id)
        
        if not entry:
            return None
        
        # Check if expired
        if time.time() - entry["created"] > TTL_SECONDS:
            del _store[layer_id]
            return None
        print(f"[Layer] Retrieving: {layer_id}")
        return {
            "sql": entry["sql"],
            "name": entry["name"]
        }

def cleanup_expired() -> int:
    now = time.time()
    
    with _lock:
        expired = [
            layer_id for layer_id, entry in _store.items()
            if now - entry["created"] > TTL_SECONDS
        ]
        
        for layer_id in expired:
            del _store[layer_id]
    
    return len(expired)