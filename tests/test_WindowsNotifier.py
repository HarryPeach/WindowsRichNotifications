"""Unit tests for the WindowsNotifier class"""
from winrichnotify import WindowsNotifier
from expects import expect, raise_error

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
