# -*- coding: utf-8 -*-
"""
File: setup.py
Path: /
Author: Grant W
"""

from setuptools import setup

setup(name='fantasypremierleagueapi',
      version='0.1',
      description=("A Python wrapper package to interface with Fantasy "
                   "Premier League's API."),
      url='http://github.com/grantula/fantasypremierleagueapi',
      author='Grant Ward',
      author_email='walter.grant.ward@gmail.com',
      license='MIT',
      install_requires=[
      'requests==2.11.1',
      ]
      packages=['fantasypremierleagueapi'],
      zip_safe=False)
