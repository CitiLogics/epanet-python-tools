# setup script for package

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="epanet_tools",
    version="1.0.0",
    author="Sam Hatchett",
    author_email="sam.hatchett@xyleminc.com",
    description="convenience functions and tools around epanet wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/CitiLogics/epanet-python-tools"
)
