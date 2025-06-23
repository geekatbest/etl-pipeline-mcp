# debounce.py
import time

_last_triggered = 0
DEBOUNCE_INTERVAL = 10  # seconds

def should_trigger():
    global _last_triggered
    now = time.time()
    if now - _last_triggered >= DEBOUNCE_INTERVAL:
        _last_triggered = now
        return True
    return False
