[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/tk-alert)](https://pypistats.org/packages/tk-alert)

# tk-alert

Lightweight, self-contained package for sending GUI alerts using tkinter.

## Table of Contents

1. **[Introduction](#tk-alert)**  
2. **[Features](#features)**  
3. **[Usage](#usage)**  
   - **[Setup](#1-setup)**  
   - **[Example Code](#2-example-code)**  
   - **[Default Alert Design](#3-default-alert-design)**  
5. **[Roadmap Items](#roadmap-items)**  
6. **[License](#license)**  
  
## Features

🚀 Minimal setup for sending GUI alerts in a Tkinter app

🎨 Highly customizable Alert widget with a modern design by default

🛠️ Ease of use out-of-the-box
  
## Usage

This example demonstrates how to create a basic Tkinter window and utilize the `tk-alert` library to display an alert notification when a button is clicked.

### 1. Setup

First, install the library using pip:

```sh
pip install tk-alert
```

### 2. Example Code

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
### 3. Default Alert Design

<img src="https://raw.githubusercontent.com/DragosPancescu/tk-alert/1ea29609d33557d096d39468a062fed07ea59be1/resources/AlertsDesign.png" width="410" height="202">

## Roadmap Items

This package is a **work in progress**. Below is the roadmap for the upcoming developments I wish to implement:

- [ ] **Tooltip on Hover**: Whenever the text inside the alert is truncated, a tooltip should appear on hover.
- [x] **Support for Multiple Python 3 Versions**: Extend compatibility to support multiple versions of Python 3.
- [ ] **Tests**: Implement testing to ensure code reliability.
- [ ] **Configuration System for the AlertGenerator Class**: Develop a configuration system where a config object can be created and injected into the class. This will eliminate the need to pass configurations at runtime every time the `.send()` method is called.
- [ ] **Better Icon Support**: Enhance icon support, allowing users to change icons rather than relying on predefined options.
- [ ] **Minimum Width Constraint**: Implement a feature to constrain the alert with a `min_width` argument.
- [ ] **Animations**: Implement an animation system.

## License

This project is licensed under the **MIT License**. See the [LICENSE](https://github.com/DragosPancescu/tk-alert/blob/main/LICENSE.txt) file for more details.
