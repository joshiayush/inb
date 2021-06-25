import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as file:
    long_description = file.read()

build_files = []

for root, directories, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith(".py"):
            build_files.append(os.path.join(root, file)[:-3])

build_files.remove("/Python/linkedin-bot/setup")

setup(
    name="linkedin-bot",
    version="1.22.7",
    url="https://github.com/JoshiAyush/linkedin-bot",
    description="A tool to automate everything on LinkedIn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=build_files,
    author="Ayush Joshi",
    author_email="ayush854032@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Public Domain",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules :: Automation :: Selenium :: Webdriver :: Chromedirver",
    ]
)
