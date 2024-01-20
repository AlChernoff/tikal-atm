from setuptools import setup

setup(name='tikal_atm',
      version='0.0.1',
      description='ATM machine for tikal home assignment',
      packages=['tikal-atm',
                'tikal-atm.src',
                'tikal-atm.src.app',
                'tikal-atm.src.app.exceptions'],
      python_requires='>=3.8',
      install_requires=[
      ],
      zip_safe=False)