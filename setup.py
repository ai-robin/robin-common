from setuptools import find_packages, setup

setup(
    name="robin_common",
    version="19.0",
    description="Common utilities and abstractions used across Robin AI codebases.",
    url="https://github.com/ai-robin/robin_common",
    author="Robin AI",
    author_email="robin@robintech.io",
    license="",
    packages=find_packages(exclude=["tests"]),
    zip_safe=True,
)
