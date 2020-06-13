#!/usr/bin/env python3

from setuptools import setup

long_description = None
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="gap",
    packages=["gap"],
    version="1.0.0",
    license="GPL",
    description="Generated argument parser",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Dominic Ricottone",
    author_email="me@dominic-ricottone.com",
    url="git.dominic-ricottone.com/gap",
    entry_points={"console_scripts": ["gap = gap.__main__:main"]},
    install_requires=["toml>=0.10.1"],
    python_requires=">=3.6",
)

