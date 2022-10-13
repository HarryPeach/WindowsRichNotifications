"""Unit tests for the WindowsNotifier class"""
from typing import Callable
from winrichnotify import WindowsNotifier
from expects import expect, raise_error, be_within
import time

import pytest


@pytest.fixture
def notifier() -> WindowsNotifier:
    """WindowsNotifier instance to be used in each test"""
    return WindowsNotifier()


def _validate_time_taken(notif_duration: int, margin: float, measured_func: Callable):
    """Checks that a notification has taken a specific amount of time to show

    Args:
        notif_duration (int): The duration of the notification
        margin (float): The margin of error
        measured_func (Callable): The function to measure the time of
    """
    start_time: float = time.time()
    measured_func()
    observed_duration = time.time() - start_time
    expect(observed_duration).to(
        be_within(notif_duration - margin, notif_duration + margin))


def test_create_notification_without_body(notifier: WindowsNotifier) -> None:
    """Test that a notification cannot be created without a body,
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
    margin: float = 0.8

    for i in range(0, 5):
        _validate_time_taken(i, margin, lambda: notifier.notify(
            "<Example Body>", duration=i))


def test_non_blocking_notifications(notifier: WindowsNotifier) -> None:
    """Test that a notification does not block program execution

    Args:
        notifier (WindowsNotifier): The instance of WindowsNotifier to use
    """
    margin: float = 0.2
    _validate_time_taken(0, margin, lambda: notifier.notify(
        "<Example Body>", duration=0, threaded=True))
