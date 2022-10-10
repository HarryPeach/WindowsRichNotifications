"""Unit tests for the WindowsNotifier class"""
from winrichnotify import WindowsNotifier
from expects import expect, raise_error, be_within
import time

import pytest


@pytest.fixture
def notifier() -> WindowsNotifier:
    """WindowsNotifier instance to be used in each test"""
    return WindowsNotifier()


def test_create_notification_without_body(notifier: WindowsNotifier) -> None:
    """Tests that a notification cannot be created without a body,
    and instead will throw an error.

    Args:
        notifier (WindowsNotifier): The instance of WindowsNotifier to use
    """
    expect(lambda: notifier.notify("")).to(raise_error(ValueError))


def test_notification_delay(notifier: WindowsNotifier) -> None:
    """Test that a notification is shown for the appropriate amount of time, within a small window.

    Args:
        notifier (WindowsNotifier): The instance of WindowsNotifier to use
    """
    margin: float = 0.5

    def test_time(notif_duration: int):
        start_time: float = time.time()
        notifier.notify("<Example Body>", duration=notif_duration)
        observed_duration = time.time() - start_time
        expect(observed_duration).to(
            be_within(notif_duration - margin, notif_duration + margin))

    for i in range(0, 5):
        test_time(i)
