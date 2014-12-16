from setuptools import setup, find_packages
import sys, os

# Parse the version from the fiona module.
with open('mercantile/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue

open_kwds = {}
if sys.version_info > (3,):
    open_kwds['encoding'] = 'utf-8'

with open('README.rst', **open_kwds) as f:
    readme = f.read()

setup(name='mercantile',
      version=version,
      description="Spherical mercator and XYZ tile utilities",
      long_description=readme,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Sean Gillies',
      author_email='sean@mapbox.com',
      url='https://github.com/sgillies/mercantile',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['click>=3.0'],
      entry_points='''
      [console_scripts]
      mercantile=mercantile.scripts:cli
      ''')
