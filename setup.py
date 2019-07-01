"""Mercantile package build script"""

import sys

from setuptools import setup, find_packages


open_kwds = {}
if sys.version_info > (3,):
    open_kwds["encoding"] = "utf-8"

with open("mercantile/__init__.py") as f:
    for line in f:
        if "__version__" in line:
            version = line.split("=")[1].strip().strip('"').strip("'")
            continue

with open("README.rst", **open_kwds) as f:
    readme = f.read()

setup(
    name="mercantile",
    version=version,
    description="Web mercator XYZ tile utilities",
    long_description=readme,
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
    keywords="mapping, web mercator, tiles",
    author="Sean Gillies",
    author_email="sean@mapbox.com",
    url="https://github.com/mapbox/mercantile",
    license="BSD",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=["click>=3.0"],
    extras_require={
        "dev": ["check-manifest"],
        "test": ["coveralls", "pytest-cov", "pydocstyle"],
    },
    entry_points="""
      [console_scripts]
      mercantile=mercantile.scripts:cli
      """,
)
