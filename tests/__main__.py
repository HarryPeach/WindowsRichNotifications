"""Some manual tests to test the functionality of the library
"""
import logging
from winrichnotify import WindowsNotifier


def notification_title_body(notifier: WindowsNotifier) -> None:
    """Shows a sample notification with a body and a title

    Args:
        notifier (WindowsNotifier): The instance of WindowsNotifier
    """
    logging.info("Showing notification with example title and body")
    notifier.notify(
        "<Example Body>",
        "<Example Title>",
    )


def notification_with_duration(notifier: WindowsNotifier) -> None:
    """Shows notifications with varying durations

    Args:
        notifier (WindowsNotifier): The instance of WindowsNotifier
    """
    logging.info("Showing notification with 5 second duration")
    notifier.notify(
        "<5 Second Notification>",
        "<Example Title>",
        duration=5
    )
    logging.info("Showing notification with 1 second duration")
    notifier.notify(
        "<1 Second Notification>",
        "<Example Title>",
        duration=1
    )


def notification_threaded(notifier: WindowsNotifier) -> None:
    """Shows a threaded notification

    Args:
        notifier (WindowsNotifier): The instance of WindowsNotifier
    """
    logging.info("Showing a threaded notification")
    notifier.notify(
        "<Threaded Notification>",
        "<Example Title>",
        threaded=True
    )
    logging.info(
        "** This message should show before the notification has dismissed **")


if __name__ == "__main__":
    notifier = WindowsNotifier()
    logging.basicConfig(level=logging.DEBUG)

    notification_title_body(notifier)
    notification_with_duration(notifier)
    notification_threaded(notifier)
