"""
Setup script for the Financial Literacy Coach application
"""
from setuptools import setup, find_packages

setup(
    name="financial-literacy-coach",
    version="1.0.0",
    description="A CLI application to help university students develop financial literacy skills",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "colorama",  # For cross-platform color support
        "tabulate",  # For data formatting
    ],
    entry_points={
        "console_scripts": [
            "financial-coach=src.main:main",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Office/Business :: Financial",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)