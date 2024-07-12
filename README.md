[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
 
# tk-alert

Lightweight, self-contained package for sending GUI alerts using tkinter.

**Work in Progress** - This package is a work in progress. Below is the roadmap for the upcoming developments I wish to implement:

## Features
🚀 Minimal setup for sending GUI alerts in a Tkinter app

🎨 Highly customizable Alert widget with a modern design by default

🛠️ Ease of use out-of-the-box
  
## Usage

To use the `tk_alert` library in a simple Tkinter application, follow the example below. This example demonstrates how to create a basic Tkinter window and utilize the `tk_alert` library to display an alert notification when a button is clicked.

### 1. Setup

First, install the library using pip:

```sh
pip install tk_alert
```

### 2. Example code

```python
import tkinter as tk
import tk_alert as tk_a

if __name__ == "__main__":
    app = tk.Tk()
    app.geometry("800x800")

    alert_generator = tk_a.AlertGenerator(app)

    show_notification_btn = tk.Button(app)
    show_notification_btn.configure(
        text="Send Alert",
        command=lambda: alert_generator.send(
            text="Alert information: Lorem Ipsum Dolor Sit Amet",
            type=tk_a.AlertType.INFO,
            anchor=tk.NW,
            duration=5
        ),
    )
    show_notification_btn.pack()

    app.mainloop()
```

## Roadmap Items

- **Tooltip on Hover**: Whenever the text inside the alert is truncated, a tooltip should appear on hover.
- **Support for Multiple Python 3 Versions**: Extend compatibility to support multiple versions of Python 3.
- **Tests**: Implement testing to ensure code reliability.
- **Configuration System for the AlertGenerator Class**: Develop a configuration system where a config object can be created and injected into the class. This will eliminate the need to pass configurations at runtime every time the `.send()` method is called.
- **Better Icon Support**: Enhance icon support, allowing users to change icons rather than relying on predefined options.
- **Minimum Width Constraint**: Implement a feature to constrain the alert with a `min_width` argument.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
