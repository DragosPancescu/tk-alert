from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="tk_alert",
    url="https://github.com/DragosPancescu/tk-alert",
    version="0.0.2",
    description="Tkinter based package for sending GUI alerts / notifications.",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dragos Pancescu",
    author_email="dragos.pnc@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7, <3.13"
)
