|Python version| |PyPI license|

.. |Python version| image:: https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white
   :target: https://www.python.org

.. |PyPI license| image:: https://img.shields.io/pypi/l/ansicolortags.svg
   :target: https://pypi.python.org/pypi/ansicolortags/

#############
tk-alert
#############

Lightweight, self-contained package for sending GUI alerts using tkinter.

Work in Progress
================
--------------------

This package is a work in progress. Below is the roadmap for the upcoming developments I wish to implement:

Roadmap Items
-------------

- **Tooltip on Hover**: Whenever the text inside the alert is truncated, a tooltip should appear on hover.
- **Support for Multiple Python 3 Versions**: Extend compatibility to support multiple versions of Python 3.
- **Tests**: Implement testing to ensure code reliability.
- **Configuration System for the AlertGenerator Class**: Develop a configuration system where a config object can be created and injected into the class. This will eliminate the need to pass configurations at runtime every time the `.send()` method is called.
- **Better Icon Support**: Enhance icon support, allowing users to change icons rather than relying on predefined options.
- **Minimum Width Constraint**: Implement a feature to constrain the alert with a `min_width` argument.

License
=======
--------------------

This project is licensed under the MIT License. See the LICENSE file for more details.
