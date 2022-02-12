import os
import pathlib

from setuptools import setup

requirementPath = (
    pathlib.Path(__file__).parent.resolve().joinpath("requirements.txt")
)  # noqa: E501
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(
    install_requires=install_requires,
    py_modules=[
        "taxes",
    ],
    python_requires=">=3.6",
)
