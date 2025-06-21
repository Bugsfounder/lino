from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lino-clipboard",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyQt5>=5.15.0",
        "keyboard>=0.13.5",
        "pyperclip>=1.8.0",
    ],
    entry_points={
        "console_scripts": [
            # "/home/bugsfounder/workspace/lino/env/bin/lino-clipboard",
            "lino-clipboard=clipboard:main",
        ],
    },
    author="Manisha Kumari",
    description="Advanced clipboard manager for LINO project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bugsfounder/LINO",
    project_urls={
        "Documentation": "https://github.com/bugsfounder/LINO/blob/main/README.md",
        "Source": "https://github.com/bugsfounder/LINO",
        "Tracker": "https://github.com/bugsfounder/LINO/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    keywords="clipboard manager productivity qt",
    # package_data={
    #     "clipboard": ["*.ui", "*.qrc", "*.png"],
    # },
)
