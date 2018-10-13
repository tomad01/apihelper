import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "apihelper",
    version = "0.0.4",
    author = "me",
    author_email = "tomadragos96@gmail.com",
    description = ("help funcs and utilities"),
    license = "BSD",
    keywords = "example documentation tutorial",
    url = "http://...",
    packages=['apihelper'],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
