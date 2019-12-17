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
    install_requires=["google-cloud-storage>=1.23.0"],
    zip_safe=True,
)
