__all__ = ['WindowsNotifier']

import logging
import threading
import time
from os import path
from time import sleep
from pkg_resources import Requirement, resource_filename

from win32api import GetModuleHandle, PostQuitMessage
from win32con import (CW_USEDEFAULT, IDI_APPLICATION, IMAGE_ICON, LR_DEFAULTSIZE,
                      LR_LOADFROMFILE, WM_DESTROY, WM_USER, WS_OVERLAPPED, WS_SYSMENU)
from win32gui import (CreateWindow, DestroyWindow, LoadIcon, LoadImage, NIF_ICON, NIF_INFO,
                      NIF_MESSAGE, NIF_TIP, NIM_ADD, NIM_DELETE, NIM_MODIFY, RegisterClass,
                      UnregisterClass, Shell_NotifyIcon, UpdateWindow, WNDCLASS, PumpMessages)

# Address of private messages (https://learn.microsoft.com/en-us/windows/win32/winmsg/wm-user)
LOCAL_WM = WM_USER + 100

# Tooltip callbacks (https://learn.microsoft.com/en-us/windows/win32/api/shellapi/nf-shellapi-shell_notifyicona)
NIN_BALLOONTIMEOUT = WM_USER + 4
NIN_BALLOONUSERCLICK = WM_USER + 5

NIN_POPUPOPEN = 0x406
NIN_POPUPCLOSE = 0x407


class WindowsNotifier(object):
    """Easily create a notification for Windows 10/11
    """

    def __init__(self):
        self._thread = None

    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        """A custom message processing callback to handle notification actions

        Args:
            hwnd (int): The window handle
            msg (int): The message
            wparam (int): An additional message parameter
            lparam (int): An additional message parameter
        """
        if msg == WM_DESTROY:
            self._on_destroy(hwnd, msg, wparam, lparam)
            return

        # Fixes (https://github.com/HarryPeach/WindowsRichNotifications/issues/7)
        if msg == 0x31f:
            PostQuitMessage(0)

        if msg == LOCAL_WM:
            if lparam == NIN_BALLOONUSERCLICK:
                if self.last_callback is not None:
                    self.last_callback()
                    self.last_callback = None
                PostQuitMessage(0)
            elif lparam == NIN_BALLOONTIMEOUT:
                PostQuitMessage(0)

        logging.debug(
            f"hwnd:{hwnd:02x}, msg:0x{msg:02x}/0d{msg}, wparam:0x{wparam:02x}/0d{wparam}, lparam:0x{lparam:02x}/0d{lparam}")

    def _notify(self, title, msg,
                icon_path, duration, click_callback) -> None:
        """Show the notification

        Args:
            title (str): The title of the notification
            msg (str): The message of the notification
            icon_path (str): The path to the icon to be used in the notification
            duration (int): The duration for the notification to last
            click_callback (Callable): The callback to be used when the notification is clicked
        """
        # Register the window class.
        self.wc = WNDCLASS()
        self.hinst = self.wc.hInstance = GetModuleHandle(None)
        self.wc.lpszClassName = str("PythonTaskbarx")  # must be a string
        self.wc.lpfnWndProc = self._wnd_proc  # could also specify a wndproc.
        self.classAtom = RegisterClass(self.wc)
        style = WS_OVERLAPPED | WS_SYSMENU
        self.hwnd = CreateWindow(self.classAtom, "Taskbar", style,
                                 0, 0, CW_USEDEFAULT,
                                 CW_USEDEFAULT,
                                 0, 0, self.hinst, None)
        UpdateWindow(self.hwnd)
        self.last_callback = click_callback

        # icon
        if icon_path is not None:
            icon_path = path.realpath(icon_path)
        else:
            icon_path = resource_filename(Requirement.parse(
                "winrichnotify"), "winrichnotify/data/python.ico")
        icon_flags = LR_LOADFROMFILE | LR_DEFAULTSIZE
        try:
            hicon = LoadImage(self.hinst, icon_path,
                              IMAGE_ICON, 0, 0, icon_flags)
        except Exception as e:
            logging.error("Some trouble with the icon ({}): {}"
                          .format(icon_path, e))
            hicon = LoadIcon(0, IDI_APPLICATION)

        # Taskbar icon
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, LOCAL_WM, hicon, "Tooltip")

        Shell_NotifyIcon(NIM_ADD, nid)
        notif_start_time = time.time()
        Shell_NotifyIcon(NIM_MODIFY, (self.hwnd, 0, NIF_INFO,
                                      LOCAL_WM,
                                      hicon, "Balloon Tooltip", msg, 200,
                                      title))

        # PumpMessages handles the messages of the window in the main loop
        # but will NOT STOP until PostQuitMessage is called
        PumpMessages()

        # Ensure that the duration of the notification is correct
        while time.time() - notif_start_time < duration:
            sleep(0.1)

        DestroyWindow(self.hwnd)
        UnregisterClass(self.wc.lpszClassName, None)
        return None

    def notify(self, body, title="",
               icon_path=None, duration=5, threaded=False, click_callback=None) -> bool:
        """Shows a notification to the user

        Args:
            body (str): The body content of the notification. Cannot be blank.
            title (str, optional): What to title the notification with. Defaults to "".
            icon_path (_type_, optional): Path to the icon (.ico) used in the notification.
                                          Defaults to None.
            duration (int, optional): The duration the notification should last for in seconds.
                                      Defaults to 5. Windows 10/11 also by default only allow
                                      notifications to be on screen for a maximum of 5 seconds
                                      unless changed by the user.
            threaded (bool, optional): Whether the thread should run on its own thread, useful for
                                       non-blocking notifications. Defaults to False.
            click_callback (Callable, optional): The function to call when the notification is
                                                 clicked by a user. Defaults to None.

        Returns:
            bool: Returns False if a notification is already active
        """
        if body == "":
            raise ValueError("The body of a notification cannot be empty")

        if not threaded:
            self._notify(title, body, icon_path, duration, click_callback)
        else:
            if self.is_notification_active():
                # We have an active notification, let is finish so we don't spam them
                return False

            self._thread = threading.Thread(
                target=self._notify, args=(title, body, icon_path, duration, click_callback))
            self._thread.start()
        return True

    def is_notification_active(self) -> bool:
        """Returns true if there is a notification currently being shown

        Returns:
            bool: Whether a notification is currently being shown
        """
        if self._thread is not None and self._thread.is_alive():
            # We have an active notification, let is finish we don't spam them
            return True
        return False

    def _on_destroy(self, hwnd, msg, wparam, lparam) -> None:
        """Clean-up after notification ended."""
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0)

        return None
