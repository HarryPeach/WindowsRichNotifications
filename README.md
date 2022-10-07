# Windows Rich Notifications for Python (winrichnotify)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

An easy-to-use Python library for displaying notifications for Windows 10 and Windows 11.

![o7ja4 1](https://user-images.githubusercontent.com/4750998/192027245-5c2298c7-a036-4638-8f51-49cdb8c5b6ca.png)


## Installation

```
pip install winrichnotify
```

# Build Setup
1. Install [Poetry](https://python-poetry.org/)
2. Navigate to the root directory of the project and run ```poetry install```. This will install the dependencies for the project
3. Run ```poetry build``` to generate built releases of the library.

## Example

```python
from winrichnotify import WindowsNotifier
notifier = WindowsNotifier()
notifier.notify("This is an example notification!",
                "With an example title!",
                icon_path="custom.ico",
                duration=10)

notifier.notify("Another notification!",
                "With yet another title!",
                icon_path=None,
                duration=5,
                threaded=True)

# Wait for the threaded notification to finish
while notifier.notification_active(): time.sleep(0.1)
```

## Contributing

Contributions are very welcome! To find a list of current contributors go [here](https://github.com/HarryPeach/WindowsRichNotifications/graphs/contributors)

## License
This project is protected under the MIT license, available in the LICENSE file.