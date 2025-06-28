"""Simple motion/animation primitives."""

import threading
import time
from typing import Callable


def animate(duration: float, step: Callable[[float], None]):
    """Call `step` repeatedly over `duration` seconds with progress 0..1."""
    start = time.time()

    def run():
        while True:
            now = time.time()
            t = (now - start) / duration
            if t > 1:
                t = 1
            step(t)
            if t >= 1:
                break
            time.sleep(0.016)

    threading.Thread(target=run).start()
