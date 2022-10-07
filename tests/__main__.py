"""Some manual tests to test the functionality of the library
"""
import logging
from winrichnotify import ToastNotifier


def notification_title_body(toaster: ToastNotifier) -> None:
    """Shows a sample notification with a body and a title

    Args:
        toaster (ToastNotifier): The instance of ToastNotifier
    """
    logging.info("Showing notification with example title and body")
    toaster.show_toast(
        "<Example Body>",
        "<Example Title>"
    )


def notification_with_duration(toaster: ToastNotifier) -> None:
    """Shows notifications with varying durations

    Args:
        toaster (ToastNotifier): The instance of ToastNotifier
    """
    logging.info("Showing notification with 5 second duration")
    toaster.show_toast(
        "<5 Second Notification>",
        "<Example Title>",
        duration=5
    )
    logging.info("Showing notification with 1 second duration")
    toaster.show_toast(
        "<1 Second Notification>",
        "<Example Title>",
        duration=1
    )


def notification_threaded(toaster: ToastNotifier) -> None:
    """Shows a threaded notification

    Args:
        toaster (ToastNotifier): The instance of ToastNotifier
    """
    logging.info("Showing a threaded notification")
    toaster.show_toast(
        "<Threaded Notification>",
        "<Example Title>",
        threaded=True
    )
    logging.info(
        "** This message should show before the notification has dismissed **")


if __name__ == "__main__":
    toaster = ToastNotifier()
    logging.basicConfig(level=logging.DEBUG)

    notification_title_body(toaster)
    notification_with_duration(toaster)
    notification_threaded(toaster)
