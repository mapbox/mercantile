from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='mercantile',
      version=version,
      description="Spherical mercator and XYZ tile utilities",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Sean Gillies',
      author_email='sean@mapbox.com',
      url='https://github.com/sgillies/mercantile',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
