from setuptools import setup, find_packages

setup(name='pyirishrail',
      version='0.0.2',
      description='Python library to get the real-time transport information (RTPI) from Irish Rail',
      keywords='irish rail RTPI',
      author='Thom Troy',
      author_email='ttroy50@gmail.com',
      license='MIT',
      url='https://github.com/ttroy50/pyirishrail',
      download_url='https://github.com/ttroy50/pyirishrail/archive/0.0.2.tar.gz',
      platforms=["any"],
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
          'requests',
      ],
      tests_requires=[
          'tox',
          'flake8',
          'pylint',
          'pytest'
      ]
     )
