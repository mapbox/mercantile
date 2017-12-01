from setuptools import setup, find_packages
import os
import sys

open_kwds = {}
if sys.version_info > (3,):
    open_kwds['encoding'] = 'utf-8'

with open('README.rst', **open_kwds) as f:
    readme = f.read()

setup(name='mercantile',
      version='1.0.0',
      description="Web mercator XYZ tile utilities",
      long_description=readme,
      classifiers=[
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3'],
      keywords='mapping, web mercator, tiles',
      author='Sean Gillies',
      author_email='sean@mapbox.com',
      url='https://github.com/mapbox/mercantile',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['click>=3.0'],
      entry_points='''
      [console_scripts]
      mercantile=mercantile.scripts:cli
      ''')
