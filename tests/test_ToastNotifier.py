"""Unit tests for the ToastNotifier class"""
from winrichnotify import ToastNotifier
from expects import expect, raise_error

import pytest


@pytest.fixture
def toaster() -> ToastNotifier:
    """ToastNotifier instance to be used in each test"""
    return ToastNotifier()


def test_create_notification_without_body(toaster: ToastNotifier) -> None:
    """Tests that a notification cannot be created without a body,
    and instead will throw an error.

    Args:
        toaster (ToastNotifier): The instance of ToastNotifier to use
    """
    expect(lambda: toaster.show_toast("")).to(raise_error(ValueError))
