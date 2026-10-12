"""Shared test setup.

Every test gets a time limit, so a search stuck in an infinite loop fails
with a clear message instead of hanging. The limit uses Unix signals; on
Windows it is skipped and a stuck test simply hangs (stop it with Ctrl+C).
"""

import signal

import pytest

TIME_LIMIT_SECONDS = 10


@pytest.fixture(autouse=True)
def time_limit():
    if not hasattr(signal, "SIGALRM"):
        yield
        return

    def on_timeout(signum, frame):
        raise TimeoutError(
            f"Test took more than {TIME_LIMIT_SECONDS} s: is your search "
            "looping forever, or missing a cycle check / reached table?")

    old_handler = signal.signal(signal.SIGALRM, on_timeout)
    signal.alarm(TIME_LIMIT_SECONDS)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)
