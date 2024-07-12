from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="tk_alert",
    version="0.0.1",
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
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.10"
)
